# distance_estimator.py
def estimate_distance(known_width_cm, focal_length, pixel_width):
    if pixel_width == 0: return 9999
    return (known_width_cm * focal_length) / pixel_width  # returns in cm

