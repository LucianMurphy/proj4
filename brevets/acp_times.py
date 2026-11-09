"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

SPEED_TABLE = [
   (0,200,15,34),
   (200, 400, 15, 32),
   (400, 600, 15, 30),
   (600, 1000, 11.428, 28),
   (1000, 1300, 13.333, 26),
]

FINISH_CLOSE = {
   200: (13, 30),
   300: (20, 0),
   400: (27, 0),
   600: (40, 0),
   1000: (75, 0)
}

VALID_BREVETS = set(FINISH_CLOSE)

MAX_OVERSHOOT = 1.2

def validate(control, brevet_dist):
   #makes sure inputs will work
    if brevet_dist not in VALID_BREVETS:
        raise ValueError("Brevet distance must be one of {}".format(sorted(VALID_BREVETS)))
    if control < 0:
        raise ValueError("Control distance cannot be negative")
    if control > brevet_dist * MAX_OVERSHOOT:
        raise ValueError("Control is more than 20% past the brevet distance")
    return min(control,brevet_dist)

def hours_over_dist(dist, speed):
   #sum time to ride dist
   hours = 0.0
   for start, end, *speeds in SPEED_TABLE:
      if dist <= start:
         break
      hours += (min(dist, end) - start) / speeds[speed]
   return hours

def to_iso(brevet_start, hours = 0, minutes = None):
   #shifts start time to return ISO string
   start = arrow.get(brevet_start)
   if minutes is None:
      total_minutes = round(hours * 60)
   else:
      total_minutes = hours*60 + minutes
   return start.shift(minutes = total_minutes).isoformat()

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    dist = validate(control_dist_km, brevet_dist_km)
    return to_iso(brevet_start_time, hours_over_dist(dist, 1))


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    dist = validate(control_dist_km, brevet_dist_km)
    if dist >= brevet_dist_km:
        h, m = FINISH_CLOSE[brevet_dist_km]
        return to_iso(brevet_start_time, h, m)

    if dist <= 60:
      return to_iso(brevet_start_time, dist / 20 +1)

    return to_iso(brevet_start_time, hours_over_dist(dist, 0))

   

