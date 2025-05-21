import reflex as rx
from app.state import ProjectileState


def input_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Initial Velocity (m/s):",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                name="initial_velocity",
                type="number",
                default_value=ProjectileState.initial_velocity.to_string(),
                placeholder="e.g., 20",
                step="0.1",
                required=True,
                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Launch Angle (degrees):",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                name="launch_angle",
                type="number",
                default_value=ProjectileState.launch_angle_deg.to_string(),
                placeholder="e.g., 45",
                step="0.1",
                min="0",
                max="90",
                required=True,
                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Initial Height (m):",
                class_name="block text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                name="initial_height",
                type="number",
                default_value=ProjectileState.initial_height.to_string(),
                placeholder="e.g., 0",
                step="0.1",
                min="0",
                required=True,
                class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            ),
            class_name="mb-4",
        ),
        rx.el.button(
            "Calculate Trajectory",
            type="submit",
            class_name="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500",
        ),
        on_submit=ProjectileState.handle_form_submit,
        reset_on_submit=True,
        class_name="p-6 bg-gray-100 rounded-lg shadow-md",
    )