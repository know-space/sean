import math
import numpy as np

def tle_to_cartesian(tle_str):
    # Constants
    GM = 3.986004418 * 10**14  # m^3/s^2, Earth gravitational constant
    RE = 6378137.0  # m, Earth radius
    J2 = 1.082626925638815e-3  # Earth's second gravitational constant

    # Parse the TLE string
    lines = tle_str.strip().split("\n")
    sat_name = lines[0]
    line1 = lines[1]
    line2 = lines[2]

    # Extract the orbital elements
    inclination = float(line2[13:17].strip())
    print(f"Inc: {inclination}")

    raan = float(line2[20:26].strip())
    print(f"RAAN: {raan}")

    eccentricity = float("0." + line2[33:37].strip())
    print(f"Ecc: {eccentricity}")

    argument_of_perigee = float(line2[38:46].strip())
    print(f"Arg of Peri: {argument_of_perigee}")

    mean_anomaly = float(line2[47:55].strip())
    print(f"Mean Anomaly: {mean_anomaly}")

    mean_motion = float(line2[56:67].strip())
    print(f"Mean motion: {mean_motion}")

    # Compute the semi-major axis and period
    a = (GM / (4 * math.pi**2) * (mean_motion * 60)**2)**(1/3)
    T = 2 * math.pi * math.sqrt(a**3 / GM)

    # Compute the mean anomaly at epoch
    epoch = line1[20:32].strip()
    print(f"Epoch: {epoch}")

    year = int(epoch[0:2]) + 2000
    print(f"Year: {year}")

    day_of_year = float(epoch[2:])
    print(f"DOY: {day_of_year}")

    days_since_epoch = (365 * (year - 2000) + math.floor((year - 2000) / 4) + day_of_year - 1) * 86400
    print(f"Days since epoch: {days_since_epoch}")

    mean_anomaly_epoch = mean_anomaly + (mean_motion * 360 * days_since_epoch / T) % 360
    print(f"Mean Anom Epoch: {mean_anomaly_epoch}")

    # Compute the eccentric anomaly
    E = mean_anomaly_epoch
    while True:
        E_new = E + (mean_anomaly_epoch + eccentricity * math.sin(math.radians(E)) - E) / (1 - eccentricity * math.cos(math.radians(E)))
        if abs(E_new - E) < 1e-8:
            break
        E = E_new
    E = math.radians(E)

    # Compute the position and velocity vectors in the orbital plane
    p = a * (1 - eccentricity**2)
    r = p / (1 + eccentricity * math.cos(E))
    x_orb = r * math.cos(E)
    y_orb = r * math.sin(E)
    v_orb = math.sqrt(GM * p) / r
    vx_orb = -v_orb * math.sin(E)
    vy_orb = v_orb * (eccentricity + math.cos(E))

    # Compute the transformation matrix from the orbital plane to the Earth-fixed frame
    rot1 = np.array([[math.cos(argument_of_perigee), math.sin(argument_of_perigee), 0],
                     [-math.sin(argument_of_perigee), math.cos(argument_of_perigee), 0],
                     [0, 0, 1]])
    rot2 = np.array([[1, 0, 0],
                     [0, math.cos(inclination), math.sin(inclination)],
                     [0, -math.sin(inclination), math.cos(inclination)]])
    rot3 = np.array([[math.cos(raan), math.sin(raan), 0],
                     [-math.sin(raan), math.cos(raan), 0],
                     [0, 0, 1]])
    Q = rot1.dot(rot2).dot(rot3)

    # Compute the position and velocity vectors in the Earth-fixed frame
    r_ecef = Q.dot(np.array([x_orb, y_orb, 0]))
    v_ecef = Q.dot(np.array([vx_orb, vy_orb, 0]))

    # Compute the angular velocity vector of the Earth
    w = np.array([0, 0, 7.2921150e-5])

    # Compute the position and velocity vectors relative to the Earth's center of mass
    r_eci = r_ecef
    v_eci = v_ecef - np.cross(w, r_ecef)

    # Convert to kilometers and kilometers per second
    r_km = r_eci / 1000
    v_km_s = v_eci / 1000

    # Save the results to a file
    with open("cartesian_coords.txt", "w") as f:
        f.write(f"SATNAME: {sat_name}\n")
        f.write(f"X: {r_km[0]:.6f}\n")
        f.write(f"Y: {r_km[1]:.6f}\n")
        f.write(f"Z: {r_km[2]:.6f}\n")
        f.write(f"VX: {v_km_s[0]:.6f}\n")
        f.write(f"VY: {v_km_s[1]:.6f}\n")
        f.write(f"VZ: {v_km_s[2]:.6f}\n")

tle_str = """ISS (ZARYA)
    1 25544U 98067A   21057.27679040  .00000975  00000-0  26298-4 0  9992
    2 25544  51.6447 205.0635 0002445 319.1422 221.6979 15.48920719279957"""

tle_to_cartesian(tle_str)

