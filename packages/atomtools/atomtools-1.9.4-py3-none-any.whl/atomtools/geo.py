"""
atomtools for geometry
"""
import os
import math
import itertools
import numpy as np
from numpy.linalg import norm

import modlog
import chemdata


BASEDIR = os.path.dirname(os.path.abspath(__file__))
EXTREME_SMALL = 1e-5


logger = modlog.getLogger(__name__)


def cos(theta, arc=False):
    factor = 1 if arc else math.pi/180.0
    return math.cos(theta * factor)


def sin(theta, arc=False):
    factor = 1 if arc else math.pi/180.0
    return math.sin(theta * factor)


def acos(result, arc=False):
    factor = 1 if arc else 180.0/math.pi
    return math.acos(result) * factor


def asin(result, arc=False):
    factor = 1 if arc else 180.0/math.pi
    return math.asin(result) * factor


def get_positions(positions):
    if hasattr(positions, 'positions'):
        positions = positions.positions
    return np.array(positions).reshape((-1, 3))


def get_atoms_size(positions):
    if hasattr(positions, 'positions'):
        positions = positions.positions
    assert isinstance(positions, (np.ndarray, list)
                      ), 'Please give Atoms, list or ndarray'
    positions = np.array(positions).reshape((-1, 3))
    size = [0.] * 3
    for i in range(3):
        size[i] = positions[:, i].max() - positions[:, i].min()
    return tuple(size)


def normed(v):
    v = np.array(v)
    if norm(v) < EXTREME_SMALL:
        return v
    return v/norm(v)


def vector_angle(a, b):
    return acos(np.dot(a, b)/(norm(a)*norm(b)))


def get_distance(positions, i, j):
    positions = get_positions(positions)
    return norm(positions[i]-positions[j])


def get_angle(positions, i, j, k):
    positions = get_positions(positions)
    v1 = positions[i] - positions[j]
    v2 = positions[k] - positions[j]
    return acos(normed(v1).dot(normed(v2)))
    return vector_angle(v1, v2)


def get_dihedral(positions, i, j, k, l):
    positions = get_positions(positions)
    v1 = normed(positions[i] - positions[j])
    v2 = normed(positions[l] - positions[k])
    vl = normed(positions[k] - positions[j])
    return acos(v1.dot(v2)) * np.sign(v2.dot(np.cross(v1, vl)))


def cartesian_to_zmatrix(positions, zmatrix_dict=None,
                         initial_num=0, indices=None):
    def get_zmat_data(zmatrix_dict, keywords):
        return zmatrix_dict[keywords] if zmatrix_dict is not None \
            and keywords in zmatrix_dict else []
    shown_length = get_zmat_data(zmatrix_dict, 'shown_length')
    shown_angle = get_zmat_data(zmatrix_dict, 'shown_angle')
    shown_dihedral = get_zmat_data(zmatrix_dict, 'shown_dihedral')
    same_length = get_zmat_data(zmatrix_dict, 'same_length')
    same_angle = get_zmat_data(zmatrix_dict, 'same_angle')
    same_dihedral = get_zmat_data(zmatrix_dict, 'same_dihedral')
    shown_length.sort()
    #shown_length = []
    #shown_angle = []
    #shown_dihedral = []

    positions = np.array(positions).reshape((-1, 3))
    natoms = len(positions)
    if indices is None:
        indices = np.arange(natoms)
    zmatrix = np.array([[[-1, -1], [-1, -1], [-1, -1]]]*natoms).tolist()
    same_bond_variables = [''] * len(same_length)
    variables = {}
    for ai in range(natoms):
        if ai == 0:
            continue
        elif ai == 1:
            zmatrix[ai][0] = [0, get_distance(positions, 0, 1)]
            continue
        for a0, a1 in shown_length:
            a0, a1 = indices[a0], indices[a1]
            logger.debug(f"{a0}, {a1}")
            if ai == a1:
                alpha = 'R_'+str(a0+initial_num)+'_'+str(a1+initial_num)
                write_variable = True
                for same_length, index in zip(same_length,
                                              range(len(same_length))):
                    # print((a0, a1), same_length)
                    if (a0, a1) in same_length:
                        # print("UES")
                        if same_bond_variables[index] == '':
                            same_bond_variables[index] = alpha
                            logger.debug(f"{index}, {same_bond_variables}")
                        else:
                            alpha = same_bond_variables[index]
                            write_variable = False
                        break
                zmatrix[ai][0] = [a0, alpha]
                if write_variable:
                    variables[alpha] = [(a0, a1), get_distance(positions, a0, a1)]
                break

        a0 = -1
        a1 = -1
        a2 = -1
        a0 = zmatrix[ai][0][0]
        if a0 == -1:
            a0 = 0
            dist = get_distance(positions, ai, a0)
            logger.debug(f'dist:, {ai}, {a0}, {dist}')
            zmatrix[ai][0] = [a0, dist]

        a1 = zmatrix[ai][1][0]
        if a1 == -1:
            for a1 in range(0, ai):
                if not a1 in [a0]:
                    break
            if a1 == -1:
                raise ValueError('a1 is still -1')
            angle = get_angle(positions, ai, a0, a1)
            logger.debug(f'angle:, {ai}, {a0}, {a1}, {angle}')
            zmatrix[ai][1] = [a1, angle]
        a2 = zmatrix[ai][2][0]
        if ai >= 3 and a2 == -1:
            for a2 in range(0, ai):
                if not a1 in [a0, a1]:
                    break
            if a2 == -1:
                raise ValueError('a2 is still -1')
            dihedral = get_dihedral(positions, ai, a0, a1, a2)
            logger.debug(f'dihedral:, {dihedral}')
            zmatrix[ai][2] = [a2, dihedral]
    if initial_num != 0:
        for zmat in zmatrix:
            for zmat_x in zmat:
                if zmat_x[0] != -1:
                    zmat_x[0] += initial_num
    logger.debug(f"{zmatrix}, {variables}, {indices}")
    return zmatrix, variables, indices


def cartesian_to_spherical(pos_o, pos_s):
    pos_o = np.array(pos_o)
    pos_s = np.array(pos_s)
    logger.debug(f'cartesian to spherical:, {pos_o}, {pos_s}')
    v_os = pos_s - pos_o
    if norm(v_os) < 0.01:
        return (0, 0, 0)
    x, y, z = v_os
    length = np.linalg.norm(v_os)
    theta = acos(z/length)
    xy_length = math.sqrt(x*x+y*y)
    logger.debug(f'xy_length, {theta}, {xy_length}')
    if xy_length < 0.05:
        phi_x = 0.0
        phi_y = 0.0
    else:
        phi_x = acos(x/xy_length)
        phi_y = asin(y/xy_length)
    if y >= 0:
        phi = phi_x
    else:
        phi = -phi_x
    return (length, theta, phi)


def spherical_to_cartesian(pos_o, length, space_angle, space_angle0=(0, 0)):
    theta, phi = space_angle
    theta0, phi0 = space_angle0
    print(f'sperical to cartesian:, {theta}, {phi}')
    pos_site = np.array(pos_o) + length * \
        np.array([sin(theta+theta0) * cos(phi+phi0),
                  sin(theta+theta0) * sin(phi+phi0),
                  cos(theta+theta0)])
    return pos_site


def rotate_site_angle(site_angle, theta, phi):
    for site_angle_i in site_angle:
        theta_i, phi_i = site_angle_i
        site_angle_i = [theta_i+theta, phi_i+phi]
    return site_angle


def input_standard_pos_transform(inp_pos, std_pos, t_vals,
                                 std_to_inp=True, is_coord=False):
    t_vals = np.array(t_vals).copy()
    std_O = np.array(std_pos)[-1].copy()
    inp_O = np.array(inp_pos)[-1].copy()
    std_pos = np.array(std_pos).copy() - std_O
    inp_pos = np.array(inp_pos).copy() - inp_O
    natoms = len(inp_pos)
    if not is_coord:
        inp_O = std_O = np.array([0, 0, 0])

    R_mat = None
    # return std_pos, inp_pos
    for selection in itertools.combinations(range(natoms-1), 3):
        selection = list(selection)
        std_m = std_pos[selection]
        inp_m = inp_pos[selection]
        if np.linalg.det(std_m) > 0.01 and np.linalg.det(inp_m) > 0.01:
            # std_m * R_mat = inp_m
            # R_mat = std_m^-1 * inp_m
            R_mat = np.dot(np.linalg.inv(std_m), inp_m)
            logger.debug(f'selections:, {selection}')
            logger.debug(f'{std_m}, {np.linalg.det(std_m)}')
            logger.debug(f'{inp_m}, {np.linalg.det(inp_m)}')
            break
    if R_mat is None:
        # dimision is less than 3
        for selection in itertools.combinations(range(natoms-1), 2):
            std_v0 = std_pos[selection[0]]
            std_v1 = std_pos[selection[1]]
            std_v2 = np.cross(std_v0, std_v1)
            std_m = np.array([std_v0, std_v1, std_v2])
            inp_v0 = inp_pos[selection[0]]
            inp_v1 = inp_pos[selection[1]]
            inp_v2 = np.cross(inp_v0, inp_v1)
            inp_m = np.array([inp_v0, inp_v1, inp_v2])
            if np.linalg.det(std_m) > 0.01:
                R_mat = np.dot(np.linalg.inv(std_m), inp_m)
                logger.debug(f'selections:, {selection}')
                break
    if R_mat is None:
        # 2 atoms
        std_v = std_pos[0]
        inp_v = inp_pos[0]
        R = np.cross(std_v, inp_v)
        R = normed(R)
        logger.debug(f'stdv, inpv:, {std_v}, {inp_v}, \nR:, {R}')
        if std_to_inp:
            return np.cross(R, t_vals-std_O)+inp_O
        else:
            return np.cross(t_vals-inp_O, R)+std_O
    else:
        # testification
        # if debug:
        #     assert((np.dot(std_pos, R_mat)-inp_pos < 0.001).all())
        #     logger.debug('test complete')
        if std_to_inp:
            return np.dot(t_vals - std_O, R_mat) + inp_O
        else:
            return np.dot(t_vals - inp_O, np.linalg.inv(R_mat)) + std_O


def get_X_Y_dist_matrix(X, Y=None):
    if Y is None:
        Y = X
    return np.sum(np.square(X), axis=1).reshape((-1, 1)) \
        + np.sum(np.square(Y), axis=1).reshape((1, -1)) - 2 * np.dot(X, Y.T)


def get_distance_matrix(positions):
    cell = None
    if hasattr(positions, 'cell'):
        cell = positions.cell
    positions = get_positions(positions)
    dist_matrix = get_X_Y_dist_matrix(positions)
    if cell is not None:
        for index in itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
            mpositions = positions + np.sum(cell * index, axis=0)
            dist_matrix = np.min(
                (dist_matrix, get_X_Y_dist_matrix(mpositions, positions)), axis=0)
            # print(dist_matrix)
    dist_matrix = np.sqrt(abs(dist_matrix))
    np.fill_diagonal(dist_matrix, 0)
    return dist_matrix


def dist_change_matrix(positions, dpos):
    # dpos = dpos.copy()
    positions = positions.copy()
    dists0 = get_distance_matrix(positions)
    dists1 = get_distance_matrix(dpos+positions)
    return dists1 - dists0


def get_contact_matrix(positions, numbers=None, bonding_distance_matrix=None,
                       n=6, m=12):
    if bonding_distance_matrix is None:
        if hasattr(positions, 'numbers'):
            numbers = positions.numbers
        assert numbers is not None
        bonding_distance_matrix = np.array(
            [chemdata.get_element_covalent(x) for x in numbers])
        bonding_distance_matrix = bonding_distance_matrix.reshape(
            (1, -1)) + bonding_distance_matrix.reshape((-1, 1))
        # bonding_distance_matrix *= 0
    # print('positions', positions)
    positions = get_positions(positions)
    distance_matrix = get_distance_matrix(positions)
    rx = distance_matrix / bonding_distance_matrix
    contact_matrix = (1 - np.power(rx, n)) / (1 - np.power(rx, m))
    logger.debug(f'distance_matrix:, {distance_matrix}\n\
                   bonding_distance_matrix:, {bonding_distance_matrix}')
    return contact_matrix


def freq_dist_change_matrix(XX, positions):
    XX = XX.copy()
    dists0 = get_distance_matrix(positions)
    return np.array([get_distance_matrix(x) for x in XX+positions]) - dists0


def get_rotation_matrix(k, theta, radians=False):
    """  使用罗德里格旋转公式 (Rodrigues' rotation formula )
    k is the unit vector of rotation axis;
    v is the rotated vector;
    Rotation Vector:
      R = Ecos(theta) + (1-cos(theta))*k*k^T + sin(theta)[[0, -kz, ky], [kz, 0, -kx], [-ky, kx, 0]];

    Reference:
    https://baike.baidu.com/item/%E7%BD%97%E5%BE%B7%E9%87%8C%E6%A0%BC%E6%97%8B%E8%BD%AC%E5%85%AC%E5%BC%8F/18878562?fr=aladdin
    """
    k = normed(k)
    if not radians:
        theta = math.radians(theta)
    kx = k[0]
    ky = k[1]
    kz = k[2]
    # k_c = k[np.newaxis].T # which now is column vector
    k_outer = np.outer(k, k)
    R = np.identity(3)*math.cos(theta) + (1-math.cos(theta))*k_outer + \
        math.sin(theta)*np.matrix([[0, -kz, ky], [kz, 0, -kx], [-ky, kx, 0]])
    return np.array(R)


def cellpar_to_cell(cellpar, ab_normal=(0, 0, 1), a_direction=None):
    """Return a 3x3 cell matrix from cellpar=[a,b,c,alpha,beta,gamma].

    Angles must be in degrees.

    The returned cell is orientated such that a and b
    are normal to `ab_normal` and a is parallel to the projection of
    `a_direction` in the a-b plane.

    Default `a_direction` is (1,0,0), unless this is parallel to
    `ab_normal`, in which case default `a_direction` is (0,0,1).

    The returned cell has the vectors va, vb and vc along the rows. The
    cell will be oriented such that va and vb are normal to `ab_normal`
    and va will be along the projection of `a_direction` onto the a-b
    plane.

    Example:

    >>> cell = cellpar_to_cell([1, 2, 4, 10, 20, 30], (0, 1, 1), (1, 2, 3))
    >>> np.round(cell, 3)
    array([[ 0.816, -0.408,  0.408],
           [ 1.992, -0.13 ,  0.13 ],
           [ 3.859, -0.745,  0.745]])

    """
    if a_direction is None:
        if np.linalg.norm(np.cross(ab_normal, (1, 0, 0))) < 1e-5:
            a_direction = (0, 0, 1)
        else:
            a_direction = (1, 0, 0)

    # Define rotated X,Y,Z-system, with Z along ab_normal and X along
    # the projection of a_direction onto the normal plane of Z.
    ad = np.array(a_direction)
    Z = normed(ab_normal)
    X = normed(ad - ad.dot(Z) * Z)
    Y = np.cross(Z, X)

    # Express va, vb and vc in the X,Y,Z-system
    alpha, beta, gamma = 90., 90., 90.
    if isinstance(cellpar, (int, float)):
        a = b = c = cellpar
    elif len(cellpar) == 1:
        a = b = c = cellpar[0]
    elif len(cellpar) == 3:
        a, b, c = cellpar
    else:
        a, b, c, alpha, beta, gamma = cellpar

    # Handle orthorhombic cells separately to avoid rounding errors
    eps = 2 * np.spacing(90.0, dtype=np.float64)  # around 1.4e-14
    # alpha
    if abs(abs(alpha) - 90) < eps:
        cos_alpha = 0.0
    else:
        cos_alpha = cos(alpha)
    # beta
    if abs(abs(beta) - 90) < eps:
        cos_beta = 0.0
    else:
        cos_beta = cos(beta)
    # gamma
    if abs(gamma - 90) < eps:
        cos_gamma = 0.0
        sin_gamma = 1.0
    elif abs(gamma + 90) < eps:
        cos_gamma = 0.0
        sin_gamma = -1.0
    else:
        cos_gamma = cos(gamma)
        sin_gamma = sin(gamma)

    # Build the cell vectors
    va = a * np.array([1, 0, 0])
    vb = b * np.array([cos_gamma, sin_gamma, 0])
    cx = cos_beta
    cy = (cos_alpha - cos_beta * cos_gamma) / sin_gamma
    cz_sqr = 1. - cx * cx - cy * cy
    assert cz_sqr >= 0
    cz = math.sqrt(cz_sqr)
    vc = c * np.array([cx, cy, cz])

    # Convert to the Cartesian x,y,z-system
    abc = np.vstack((va, vb, vc))
    T = np.vstack((X, Y, Z))
    cell = abc.dot(T)

    return cell


def cell_abc_alpha_beta_gamma_to_cartesion(params):
    if len(params) == 3:
        return np.diag(params)
    elif len(params) == 6:
        return cellpar_to_cell(params)
    elif np.array(params).shape == (3, 3):
        a, b, c, alpha, beta, gamma = params
        return a, b, c, alpha, beta, gamma
    else:
        raise ValueError("params type error")
