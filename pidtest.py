import time
import krpc

class PID(object):

	def __init__(self, P, I, D):
		self.Kp = P
		self.Ki = I
		self.Kd = D

		self.P = 0.0
		self.I = 0.0
		self.D = 0.0

		self.SetPoint = 0.0
		self.ClampI = 1.0
		self.LastTime = time.time()
		self.LastMeasure = 0.0

	def update(self, measure):
		now = time.time()
		time_change = now - self.LastTime
		if not time_change:
			time_change = 1.0

		error = self.SetPoint - measure
		self.P = error
		self.I += error
		self.I = self.clamp_i(self.I)
		self.D = (measure - self.LastMeasure) / (time_change)

		self.LastMeasure = measure
		self.LastTime = now

		time.sleep(0.01)
		
		return (self.Kp  * self.P) + (self.Ki * self.I) - (self.Kd * self.D)

	def clamp_i(self, i):
		if i > self.ClampI:
			return self.ClampI
		elif i < -self.ClampI:
			return - self.ClampI
		else:
			return i

	def setpoint(self, value):
		self.SetPoint = value
		self.I = 0.0


def main():

	conn = krpc.connect()
	sc = conn.space_center
	v = sc.active_vessel
	curr_body = v.orbit.body
	telem = v.flight(curr_body.reference_frame)

	p = PID(0.025, 0, 0.15)
	p.ClampI = 20
	p.setpoint(10)

	v.control.sas = True

	v.control.activate_next_stage()

	while True:

		planet_accel = (curr_body.gravitational_parameter)/((curr_body.equatorial_radius + telem.mean_altitude)**2)

		output = p.update(telem.surface_altitude)
		v.control.throttle = ((v.mass * planet_accel) / v.available_thrust) + output
		
		if (telem.surface_altitude > 25):
			v.control.gear = False
		else:
			v.control.gear = True


		print('Vertical V:{:03.2f}   PID returns:{:03.2f}   Throttle:{:03.2f}	D:{:03.2f}'
              .format(telem.surface_altitude,
                      output,
                      v.control.throttle,
                      p.D))

if __name__ == '__main__':
	main()
