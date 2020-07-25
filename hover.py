import time 
import krpc

def main():
	conn = krpc.connect()
	sc = conn.space_center
	v = sc.active_vessel
	cb = v.orbit.body
	telem = v.flight(v.orbit.body.reference_frame)

	v.control.sas = True

	while True:
		throttle_hover = (v.mass * (cb.gravitational_parameter/(float(cb.equatorial_radius) + telem.mean_altitude)**2)) / (v.available_thrust) - 0.0035
		v.control.throttle = throttle_hover
		print throttle_hover
		time.sleep(0.1)

if __name__ == '__main__':
	main()
	print('--')