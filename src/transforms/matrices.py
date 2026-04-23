import math
import pygame


def _mat_mul(a, b):
    result = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += a[i][k] * b[k][j]
    return result


def _apply(matrix, x, y):
    rx = matrix[0][0] * x + matrix[0][1] * y + matrix[0][2]
    ry = matrix[1][0] * x + matrix[1][1] * y + matrix[1][2]
    return rx, ry


# --- The four required geometric transformations ---

def translation_matrix(dx, dy):
    """T(dx, dy) — move a point by (dx, dy)."""
    return [
        [1, 0, dx],
        [0, 1, dy],
        [0, 0,  1],
    ]


def rotation_matrix(angle_rad):
    """R(θ) — rotate counter-clockwise around the origin."""
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    return [
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1],
    ]


def scale_matrix(sx, sy):
    """S(sx, sy) — scale by sx horizontally and sy vertically."""
    return [
        [sx,  0, 0],
        [ 0, sy, 0],
        [ 0,  0, 1],
    ]


def reflection_matrix_y():
    """Reflect across the vertical axis (horizontal flip, x → -x)."""
    return [
        [-1, 0, 0],
        [ 0, 1, 0],
        [ 0, 0, 1],
    ]


def reflection_matrix_x():
    """Reflect across the horizontal axis (vertical flip, y → -y)."""
    return [
        [1,  0, 0],
        [0, -1, 0],
        [0,  0, 1],
    ]


def compose(*matrices):
    """Combine multiple transforms into one by left-to-right multiplication."""
    result = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for m in matrices:
        result = _mat_mul(result, m)
    return result


def apply_transform(matrix, x, y):
    """Apply a 3×3 homogeneous matrix to point (x, y). Returns (rx, ry)."""
    return _apply(matrix, x, y)


# --- Game-level helpers that use the matrices above ---

def orbit_position(center_x, center_y, radius, angle_rad):
    """
    Compute the world position of an orbiting object.

    Uses R(angle) applied to the offset vector (radius, 0),
    then T(center) to move it into world space.

    Combined matrix: T · R
    """
    t = translation_matrix(center_x, center_y)
    r = rotation_matrix(angle_rad)
    m = compose(r, t)
    return apply_transform(m, radius, 0)


def mirror_position(player_x, arena_center_x):
    """
    Compute the mirror enemy's X position by reflecting the player
    across the vertical center line of the arena.

    Reflection across x = arena_center_x:
      1. Translate so center is at origin  T(-cx, 0)
      2. Reflect across Y axis              Ry
      3. Translate back                     T(cx, 0)
    """
    t_in  = translation_matrix(-arena_center_x, 0)
    ref   = reflection_matrix_y()
    t_out = translation_matrix( arena_center_x, 0)
    m = compose(t_in, ref, t_out)
    rx, _ = apply_transform(m, player_x, 0)
    return rx


def scale_surface(surface, sx, sy):
    """
    Scale a pygame Surface by (sx, sy) using pygame.transform.scale,
    mirroring the S(sx, sy) matrix operation in screen space.
    """
    w = int(surface.get_width()  * sx)
    h = int(surface.get_height() * sy)
    return pygame.transform.scale(surface, (w, h))


def rotate_surface(surface, angle_deg):
    """
    Rotate a pygame Surface by angle_deg counter-clockwise,
    mirroring the R(θ) matrix operation.
    """
    return pygame.transform.rotate(surface, angle_deg)


def flip_surface(surface, flip_x=True, flip_y=False):
    """
    Flip a pygame Surface, mirroring the reflection matrix operation.
    flip_x=True  → horizontal flip (reflects across vertical axis)
    flip_y=True  → vertical flip   (reflects across horizontal axis)
    """
    return pygame.transform.flip(surface, flip_x, flip_y)
