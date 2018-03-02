from hashcode import FileIO, Logger
import time

def get_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

class Ride:
    def __init__(self, start_row, start_col, end_row, end_col, earliest_start, latest_finish, id):
        self.start = [start_row, start_col]
        self.end = [end_row, end_col]
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.dist = get_dist(self.start, self.end)
        self.time_frame = self.latest_finish - self.earliest_start
        self.spare_time = self.time_frame - self.dist
        self.id = id


    def print(self):
        print("Ride Data\n------------------")
        print("Start Position: {}".format(self.start))
        print("Final Position: {}".format(self.end))
        print("Earliest Start: {}".format(self.earliest_start))
        print("Latest Finish: {}".format(self.latest_finish))
        print("Distance: {}".format(self.dist))
        print("------------------\n")

class Vehicle:
    def __init__(self):
        self.pos = [0, 0]
        self.available = True
        self.cycleDone = -1
        self.backlog = []

    def assign_ride(self, ride, cycleDone):
        self.available = False
        self.pos = ride.end
        self.cycleDone = cycleDone
        self.add_to_backlog(ride.id)

    def remove_ride(self):
        self.available = True
        self.cycleDone = -1

    def add_to_backlog(self, id):
        self.backlog.append(id)

class Simulation:
    def __init__(self, file, sample_size):
        self.file = FileIO(file, "rw")
        self.logger = Logger()
        rows, columns, no_vehicles, no_rides, bonus, steps = self.file.readList(0)
        self.rides = []
        self.vehicles = []
        self.map_size = [rows, columns]
        self.no_vehicles = no_vehicles
        self.no_rides = no_rides
        self.bonus = bonus
        self.T = 0
        self.max_steps = steps
        self.sample_size = sample_size
        self.init_time = time.time()

        for i in range(no_rides):
            s_r, s_c, e_r, e_c, e_s, l_f = self.file.readList(1 + i)
            self.rides.append(Ride(s_r, s_c, e_r, e_c, e_s, l_f, i))

        for i in range(no_vehicles):
            self.vehicles.append(Vehicle())

        # Sort the rides by earliest start
        self.rides.sort(key=lambda x: x.earliest_start)

    def print_status(self):
        self.logger.printParameters({
            "Map: ": self.map_size,
            "Vehicles": self.no_vehicles,
            "Rides: ": self.no_rides
        })

    def find_ride(self, vehicle):
        # Remove the rides that have become too old
        while self.rides[0].latest_finish <= self.T:
            del self.rides[0]


        best_dist = -1
        ride_counter = 0
        best_offset = 0
        offset = 0
        while ride_counter < self.sample_size:
            while get_dist(vehicle.pos, self.rides[offset].start) + self.rides[offset].dist + self.T > self.rides[offset].latest_finish:
                offset += 1
            total_dist = get_dist(vehicle.pos, self.rides[offset].start) + self.rides[offset].dist


            if total_dist < best_dist or best_dist < 0:
                best_offset = offset
                best_dist = total_dist

            ride_counter += 1

        vehicle.assign_ride(self.rides[best_offset], self.T + best_dist)
        del self.rides[best_offset]

    def assign_rides(self):
        for vehicle in self.vehicles:
            if vehicle.available and len(self.rides) != 0:
                self.find_ride(vehicle)
            elif vehicle.cycleDone >= self.T:
                vehicle.remove_ride()

    def next_timestep(self):
        self.assign_rides()
        self.T += 1

    def run(self):
        for i in range(self.max_steps):
            self.next_timestep()

        final_time = time.time()
        print(final_time - self.init_time)
        self.write_file()

    def write_file(self):
        for vehicle in self.vehicles:
            x = [len(vehicle.backlog)]
            x.extend(vehicle.backlog)
            self.file.writeList(x)
        self.file.writeClose()





sim = Simulation("c_no_hurry", 1000)
sim.print_status()

sim.run()








