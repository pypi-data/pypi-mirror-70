#!/usr/bin/env python3
# coding: utf-8
"""
Created on Thu Sep 13 2018
@author: Nathan de Lara <ndelara@enst.fr>
@author: Thomas Bonald <bonald@enst.fr>
"""
import warnings
from typing import Union

import numpy as np
from scipy import sparse

from sknetwork.embedding.base import BaseEmbedding, BaseBiEmbedding
from sknetwork.linalg import EigSolver, HalkoEig, LanczosEig, auto_solver, diag_pinv, normalize, LaplacianOperator,\
    NormalizedAdjacencyOperator, RegularizedAdjacency
from sknetwork.utils.check import check_format, check_square, check_symmetry, check_adjacency_vector, is_connected,\
    check_nonnegative, check_n_components
from sknetwork.utils.format import bipartite2undirected


class Spectral(BaseEmbedding):
    """Spectral embedding of graphs, based the spectral decomposition of the Laplacian matrix :math:`L = D - A`.
    Eigenvectors are considered in increasing order of eigenvalues, skipping the first eigenvector.

    * Graphs

    See :class:`BiSpectral` for digraphs and bigraphs.

    Parameters
    ----------
    n_components : int (default = 2)
        Dimension of the embedding space.
    normalized_laplacian : bool (default = ``True``)

        * If ``True``, solve the eigenvalue problem :math:`LU = DU \\Lambda`.
        * If ``False``, solve the eigenvalue problem :math:`LU = U \\Lambda`.

    regularization : ``None`` or float (default = ``0.01``)
        Add edges of given weight between all pairs of nodes.
    relative_regularization : bool (default = ``True``)
        If ``True``, consider the regularization as relative to the total weight of the graph.
    equalize : bool (default = ``False``)
        If ``True``, equalize the energy levels of the corresponding physical system, i.e., use
        :math:`U \\Lambda^{- \\frac 1 2}`. Require regularization if the graph is not connected.
    barycenter : bool (default = ``True``)
        If ``True``, use the barycenter of neighboring nodes for the embedding, i.e., :math:`PU`
        with :math:`P = D^{-1}A`. Otherwise, use :math:`U`.
    normalized : bool (default = ``True``)
        If ``True``, normalized the embedding so that each vector has norm 1 in the embedding space, i.e.,
        each vector lies on the unit sphere.
    solver : ``'auto'``, ``'halko'``, ``'lanczos'`` or :class:`EigSolver` (default = ``'auto'``)
        Which eigenvalue solver to use.

        * ``'auto'`` call the auto_solver function.
        * ``'halko'``: randomized method, fast but less accurate than ``'lanczos'`` for ill-conditioned matrices.
        * ``'lanczos'``: power-iteration based method.
        * :class:`EigSolver`: custom solver.

    Attributes
    ----------
    embedding_ : array, shape = (n, n_components)
        Embedding of the nodes.
    eigenvalues_ : array, shape = (n_components)
        Eigenvalues in increasing order (first eigenvalue ignored).
    eigenvectors_ : array, shape = (n, n_components)
        Corresponding eigenvectors.
    regularization_ : ``None`` or float
        Regularization factor added to all pairs of nodes.

    Example
    -------
    >>> from sknetwork.embedding import Spectral
    >>> from sknetwork.data import karate_club
    >>> spectral = Spectral()
    >>> adjacency = karate_club()
    >>> embedding = spectral.fit_transform(adjacency)
    >>> embedding.shape
    (34, 2)

    References
    ----------
    Belkin, M. & Niyogi, P. (2003). Laplacian Eigenmaps for Dimensionality Reduction and Data Representation,
    Neural computation.
    """
    def __init__(self, n_components: int = 2, normalized_laplacian=True,
                 regularization: Union[None, float] = 0.01, relative_regularization: bool = True,
                 equalize: bool = False, barycenter: bool = True, normalized: bool = True,
                 solver: Union[str, EigSolver] = 'auto'):
        super(Spectral, self).__init__()

        self.n_components = n_components
        self.normalized_laplacian = normalized_laplacian

        if regularization == 0:
            self.regularization = None
        else:
            self.regularization = regularization
        self.relative_regularization = relative_regularization

        self.equalize = equalize
        self.barycenter = barycenter
        self.normalized = normalized
        if solver == 'halko':
            self.solver: EigSolver = HalkoEig()
        elif solver == 'lanczos':
            self.solver: EigSolver = LanczosEig()
        else:
            self.solver = solver

        self.eigenvalues_ = None
        self.eigenvectors_ = None
        self.regularization_ = None

    def fit(self, adjacency: Union[sparse.csr_matrix, np.ndarray]) -> 'Spectral':
        """Compute the graph embedding.

        Parameters
        ----------
        adjacency :
              Adjacency matrix of the graph (symmetric matrix).

        Returns
        -------
        self: :class:`Spectral`
        """
        adjacency = check_format(adjacency).asfptype()
        check_square(adjacency)
        check_symmetry(adjacency)
        n = adjacency.shape[0]

        if self.solver == 'auto':
            solver = auto_solver(adjacency.nnz)
            if solver == 'lanczos':
                self.solver: EigSolver = LanczosEig()
            else:  # pragma: no cover
                self.solver: EigSolver = HalkoEig()

        n_components = check_n_components(self.n_components, n-2)
        n_components += 1

        if self.equalize and (self.regularization is None or self.regularization == 0.) and not is_connected(adjacency):
            raise ValueError("The option 'equalize' is valid only if the graph is connected or with regularization."
                             "Call 'fit' either with 'equalize' = False or positive 'regularization'.")

        weights = adjacency.dot(np.ones(n))
        regularization = self.regularization
        if regularization:
            if self.relative_regularization:
                regularization = regularization * weights.sum() / n ** 2
            weights += regularization * n

        if self.normalized_laplacian:
            # Finding the largest eigenvalues of the normalized adjacency is easier for the solver than finding the
            # smallest eigenvalues of the normalized laplacian.
            weights_inv_sqrt_diag = diag_pinv(np.sqrt(weights))

            if regularization:
                norm_adjacency = NormalizedAdjacencyOperator(adjacency, regularization)
            else:
                norm_adjacency = weights_inv_sqrt_diag.dot(adjacency.dot(weights_inv_sqrt_diag))

            self.solver.which = 'LA'
            self.solver.fit(matrix=norm_adjacency, n_components=n_components)
            eigenvalues = 1 - self.solver.eigenvalues_
            # eigenvalues of the Laplacian in increasing order
            index = np.argsort(eigenvalues)[1:]
            # skip first eigenvalue
            eigenvalues = eigenvalues[index]
            # eigenvectors of the Laplacian, skip first eigenvector
            eigenvectors = np.array(weights_inv_sqrt_diag.dot(self.solver.eigenvectors_[:, index]))

        else:
            if regularization:
                laplacian = LaplacianOperator(adjacency, regularization)
            else:
                weight_diag = sparse.diags(weights, format='csr')
                laplacian = weight_diag - adjacency

            self.solver.which = 'SM'
            self.solver.fit(matrix=laplacian, n_components=n_components)
            eigenvalues = self.solver.eigenvalues_[1:]
            eigenvectors = self.solver.eigenvectors_[:, 1:]

        embedding = eigenvectors.copy()

        if self.equalize:
            eigenvalues_sqrt_inv_diag = diag_pinv(np.sqrt(eigenvalues))
            embedding = eigenvalues_sqrt_inv_diag.dot(embedding.T).T

        if self.barycenter:
            eigenvalues_diag = sparse.diags(eigenvalues)
            subtract = eigenvalues_diag.dot(embedding.T).T
            if not self.normalized_laplacian:
                weights_inv_diag = diag_pinv(weights)
                subtract = weights_inv_diag.dot(subtract)
            embedding -= subtract

        if self.normalized:
            embedding = normalize(embedding, p=2)

        self.embedding_ = embedding
        self.eigenvalues_ = eigenvalues
        self.eigenvectors_ = eigenvectors
        self.regularization_ = regularization

        return self

    def predict(self, adjacency_vectors: Union[sparse.csr_matrix, np.ndarray]) -> np.ndarray:
        """Predict the embedding of new nodes, defined by their adjacency vectors.

        Parameters
        ----------
        adjacency_vectors :
            Adjacency vectors of nodes.
            Array of shape (n_col,) (single vector) or (n_vectors, n_col)

        Returns
        -------
        embedding_vectors : np.ndarray
            Embedding of the nodes.
        """
        self._check_fitted()
        eigenvectors = self.eigenvectors_
        eigenvalues = self.eigenvalues_
        n = eigenvectors.shape[0]

        adjacency_vectors = check_adjacency_vector(adjacency_vectors, n)
        check_nonnegative(adjacency_vectors)

        # regularization
        if self.regularization_:
            adjacency_vectors = RegularizedAdjacency(adjacency_vectors, self.regularization_)

        # projection in the embedding space
        averaging = normalize(adjacency_vectors, p=1)
        embedding_vectors = averaging.dot(eigenvectors)

        if not self.barycenter:
            if self.normalized_laplacian:
                factors = 1 - eigenvalues
            else:
                # to be modified
                factors = 1 - eigenvalues / (adjacency_vectors.sum() + 1e-9)
            factors_inv_diag = diag_pinv(factors)
            embedding_vectors = factors_inv_diag.dot(embedding_vectors.T).T

        if self.equalize:
            embedding_vectors = diag_pinv(np.sqrt(eigenvalues)).dot(embedding_vectors.T).T

        if self.normalized:
            embedding_vectors = normalize(embedding_vectors, p=2)

        if embedding_vectors.shape[0] == 1:
            embedding_vectors = embedding_vectors.ravel()

        return embedding_vectors


class BiSpectral(Spectral, BaseBiEmbedding):
    """Spectral embedding of bipartite graphs, based the spectral decomposition of the Laplacian matrix
    :math:`L = D - A` with :math:`A` the adjacency matrix of the graph. Eigenvectors are considered in increasing order
    of eigenvalues, skipping the first eigenvector.

    * Digraphs
    * Bigraphs

    Parameters
    ----------
    n_components : int (default = 2)
        Dimension of the embedding space.
    normalized_laplacian : bool (default = ``True``)

        * If ``True``, solve the eigenvalue problem :math:`LU = DU \\Lambda`.
        * If ``False``, solve the eigenvalue problem :math:`LU = U \\Lambda`.

    regularization : ``None`` or float (default = ``0.01``)
        Add edges of given weight between all pairs of nodes.
    relative_regularization : bool (default = ``True``)
        If ``True``, consider the regularization as relative to the total weight of the graph.
    equalize : bool (default = ``False``)
        If ``True``, equalize the energy levels of the corresponding physical system, i.e., use
        :math:`U \\Lambda^{- \\frac 1 2}`. Requires regularization if the graph is not connected.
    barycenter : bool (default = ``True``)
        If ``True``, use the barycenter of neighboring nodes for the embedding, i.e., :math:`PU`
        with :math:`P = D^{-1}A`. Otherwise use :math:`U`.
    normalized : bool (default = ``True``)
        If ``True``, normalized the embedding so that each vector has norm 1 in the embedding space, i.e.,
        each vector lies on the unit sphere.
    solver : ``'auto'``, ``'halko'``, ``'lanczos'`` or :class:`EigSolver` (default = ``'auto'``)
        Which eigenvalue solver to use.

        * ``'auto'`` call the auto_solver function.
        * ``'halko'``: randomized method, fast but less accurate than ``'lanczos'`` for ill-conditioned matrices.
        * ``'lanczos'``: power-iteration based method.
        * :class:`EigSolver`: custom solver.

    Attributes
    ----------
    embedding_ : array, shape = (n_row, n_components)
        Embedding of the rows.
    embedding_row_ : array, shape = (n_row, n_components)
        Embedding of the rows (copy of **embedding_**).
    embedding_col_ : array, shape = (n_col, n_components)
        Embedding of the columns.
    eigenvalues_ : array, shape = (n_components)
        Eigenvalues in increasing order (first eigenvalue ignored).
    eigenvectors_ : array, shape = (n, n_components)
        Corresponding eigenvectors.
    regularization_ : ``None`` or float
        Regularization factor added to all pairs of nodes.

    Example
    -------
    >>> from sknetwork.embedding import BiSpectral
    >>> from sknetwork.data import movie_actor
    >>> bispectral = BiSpectral()
    >>> biadjacency = movie_actor()
    >>> embedding = bispectral.fit_transform(biadjacency)
    >>> embedding.shape
    (15, 2)

    References
    ----------
    Belkin, M. & Niyogi, P. (2003). Laplacian Eigenmaps for Dimensionality Reduction and Data Representation,
    Neural computation.
    """
    def __init__(self, n_components: int = 2, normalized_laplacian=True,
                 regularization: Union[None, float] = 0.01, relative_regularization: bool = True,
                 equalize: bool = False, barycenter: bool = True, normalized: bool = True,
                 solver: Union[str, EigSolver] = 'auto'):
        super(BiSpectral, self).__init__(n_components, normalized_laplacian, regularization, relative_regularization,
                                         equalize, barycenter, normalized, solver)

    def fit(self, biadjacency: Union[sparse.csr_matrix, np.ndarray]) -> 'BiSpectral':
        """Spectral embedding of the bipartite graph considered as undirected, with adjacency matrix:

        :math:`A  = \\begin{bmatrix} 0 & B \\\\ B^T & 0 \\end{bmatrix}`

        where :math:`B` is the input (biadjacency matrix).

        Parameters
        ----------
        biadjacency:
            Biadjacency matrix of the graph.

        Returns
        -------
        self: :class:`BiSpectral`
        """
        biadjacency = check_format(biadjacency)
        n_row, _ = biadjacency.shape
        Spectral.fit(self, bipartite2undirected(biadjacency))
        self._split_vars(n_row)

        return self

    def predict(self, adjacency_vectors: Union[sparse.csr_matrix, np.ndarray]) -> np.ndarray:
        """Predict the embedding of new rows, defined by their adjacency vectors.

        Parameters
        ----------
        adjacency_vectors :
            Adjacency vectors of nodes.
            Array of shape (n_col,) (single vector) or (n_vectors, n_col)

        Returns
        -------
        embedding_vectors : np.ndarray
            Embedding of the nodes.
        """
        self._check_fitted()
        n_row, _ = self.embedding_row_.shape
        n_col, _ = self.embedding_col_.shape

        adjacency_vectors = check_adjacency_vector(adjacency_vectors, n_col)
        empty_block = sparse.csr_matrix((adjacency_vectors.shape[0], n_row))
        adjacency_vectors = sparse.bmat([[empty_block, adjacency_vectors]], format='csr')
        embedding_vectors = Spectral.predict(self, adjacency_vectors)

        return embedding_vectors
