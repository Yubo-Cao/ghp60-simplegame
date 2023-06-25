from game.physics import calculate_contact


def handle_collision(collision, rb):
    result = calculate_collision(collision, rb)
    rb.velocity = rb.velocity.reflect(result.plane) * 0.5
    rb.acceleration = rb.acceleration.reflect(result.plane) * 0.5
    new_pos = rb.position + result.normal * result.penetration_depth
    rb.position = new_pos
    return result


def calculate_collision(collision, rb):
    result = calculate_contact(
        rb.get_rect(),
        collision.b.get_rect(),
        rb.get_velocity(),
        collision.b.get_velocity(),
    )
    return result
