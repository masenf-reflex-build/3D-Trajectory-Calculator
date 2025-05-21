import reflex as rx
import numpy as np
from typing import TypedDict, List as TypingList


class TrajectoryPoint(TypedDict):
    x: float
    y: float


class ProjectileState(rx.State):
    initial_velocity: float = 20.0
    launch_angle_deg: float = 45.0
    initial_height: float = 0.0
    gravity: float = 9.81
    time_step: float = 0.05
    trajectory_data: TypingList[TrajectoryPoint] = []
    max_height: float = 0.0
    total_range: float = 0.0
    time_of_flight: float = 0.0
    error_message: str = ""

    @rx.var
    def max_height_str(self) -> str:
        return f"{self.max_height:.2f}"

    @rx.var
    def total_range_str(self) -> str:
        return f"{self.total_range:.2f}"

    @rx.var
    def time_of_flight_str(self) -> str:
        return f"{self.time_of_flight:.2f}"

    @rx.event
    def handle_form_submit(self, form_data: dict):
        self.error_message = ""
        try:
            self.initial_velocity = float(
                form_data["initial_velocity"]
            )
            self.launch_angle_deg = float(
                form_data["launch_angle"]
            )
            initial_height_str = form_data.get(
                "initial_height", "0.0"
            )
            self.initial_height = float(
                initial_height_str
                if initial_height_str
                else "0.0"
            )
            if self.initial_velocity <= 0:
                self.error_message = (
                    "Initial velocity must be positive."
                )
                self._reset_outputs()
                return
            if not 0 <= self.launch_angle_deg <= 90:
                self.error_message = "Launch angle must be between 0 and 90 degrees."
                self._reset_outputs()
                return
            if self.initial_height < 0:
                self.error_message = (
                    "Initial height cannot be negative."
                )
                self._reset_outputs()
                return
        except ValueError:
            self.error_message = "Invalid input. Please enter numeric values."
            self._reset_outputs()
            return
        except KeyError as e:
            self.error_message = f"Missing required field: {e}. Please fill all fields."
            self._reset_outputs()
            return
        self._calculate_trajectory()

    def _reset_outputs(self):
        self.trajectory_data = []
        self.max_height = 0.0
        self.total_range = 0.0
        self.time_of_flight = 0.0

    def _calculate_trajectory(self):
        self._reset_outputs()
        angle_rad = np.deg2rad(self.launch_angle_deg)
        v0x = self.initial_velocity * np.cos(angle_rad)
        v0y = self.initial_velocity * np.sin(angle_rad)
        if self.initial_height == 0 and (
            self.launch_angle_deg == 0
            or (v0y <= 0 and v0x == 0)
        ):
            self.trajectory_data = [
                TrajectoryPoint(x=0, y=0)
            ]
            self.max_height = 0.0
            self.total_range = 0.0
            self.time_of_flight = 0.0
            return
        t = 0.0
        x = 0.0
        y_current = self.initial_height
        current_max_height = self.initial_height
        self.trajectory_data.append(
            TrajectoryPoint(x=x, y=y_current)
        )
        abs_v0y = abs(v0y)
        if self.gravity > 0:
            time_to_peak_if_positive_v0y = (
                abs_v0y / self.gravity if v0y > 0 else 0
            )
            height_at_peak = (
                self.initial_height
                + abs_v0y * time_to_peak_if_positive_v0y
                - 0.5
                * self.gravity
                * time_to_peak_if_positive_v0y**2
                if v0y > 0
                else self.initial_height
            )
            time_from_peak_to_ground = (
                np.sqrt(2 * height_at_peak / self.gravity)
                if height_at_peak >= 0
                else 0
            )
            max_sim_time = (
                time_to_peak_if_positive_v0y
                + time_from_peak_to_ground
            ) * 1.5 + 5 * self.time_step
            if max_sim_time <= self.time_step:
                max_sim_time = 100 * self.time_step
        else:
            max_sim_time = (
                1000 * self.time_step
                if v0y <= 0
                else (
                    2 * self.initial_height / abs(v0y)
                    if abs(v0y) > 0
                    else 1000 * self.time_step
                )
            )
        while True:
            t += self.time_step
            x = v0x * t
            y_new = (
                self.initial_height
                + v0y * t
                - 0.5 * self.gravity * t**2
            )
            current_max_height = max(
                current_max_height, y_new
            )
            if y_new < 0:
                y_prev = self.trajectory_data[-1]["y"]
                t_prev = t - self.time_step
                if y_prev > 0:
                    t_fraction = y_prev / (y_prev - y_new)
                    t_impact = (
                        t_prev + t_fraction * self.time_step
                    )
                    x_impact = v0x * t_impact
                    self.trajectory_data.append(
                        TrajectoryPoint(x=x_impact, y=0.0)
                    )
                    self.time_of_flight = t_impact
                    self.total_range = x_impact
                else:
                    self.trajectory_data.append(
                        TrajectoryPoint(
                            x=self.trajectory_data[-1]["x"],
                            y=0.0,
                        )
                    )
                    self.time_of_flight = t_prev
                    self.total_range = self.trajectory_data[
                        -1
                    ]["x"]
                break
            self.trajectory_data.append(
                TrajectoryPoint(x=x, y=y_new)
            )
            if t > max_sim_time:
                self.error_message = "Simulation time exceeded safety limit. Trajectory may be incomplete."
                self.time_of_flight = t
                self.total_range = x
                break
        self.max_height = current_max_height
        if len(self.trajectory_data) < 2:
            self.trajectory_data.append(
                TrajectoryPoint(
                    x=self.total_range + 0.01, y=0.0
                )
            )

    @rx.event
    def calculate_default_trajectory(self):
        self._calculate_trajectory()