from game.physics import calculate_contact
from game.utils import Number, Vector2D


def handle_collision(collision, rb, dt):
    result = calculate_collision(collision, rb)

    rb.position = rb.position + result.normal * result.penetration_depth
    rb.position += (
        rb.velocity * Vector2D[Number](abs(result.plane.x), abs(result.plane.y)) * dt
        + rb.acceleration
        * Vector2D[Number](abs(result.plane.x), abs(result.plane.y))
        * dt
    )

    rb.velocity = rb.velocity.reflect(result.plane) * 0.5
    rb.acceleration = rb.acceleration.reflect(result.plane) * 0.5
    return result


def calculate_collision(collision, rb):
    result = calculate_contact(
        rb.get_rect(),
        collision.b.get_rect(),
        rb.get_velocity(),
        collision.b.get_velocity(),
    )
    return result
