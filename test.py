import krpc

conn = krpc.connect(name='test')

vessel = conn.space_center.active_vessel

vessel.flight().surface_reference_frame = True
while True:

	print vessel.flight(vessel.orbit.body.reference_frame).vertical_speed

	if vessel.flight(vessel.orbit.body.reference_frame).vertical_speed <= 10:
		vessel.control.throttle = 1
	else:
		vessel.control.throttle = 0


