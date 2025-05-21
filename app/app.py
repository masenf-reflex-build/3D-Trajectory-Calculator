import reflex as rx
from app.state import ProjectileState
from app.components.input_form import input_form
from app.components.trajectory_plot import (
    trajectory_plot_component,
)
from rxconfig import config


def index() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                "Projectile Trajectory Calculator",
                class_name="text-4xl font-extrabold text-center my-8 text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600",
            ),
            rx.el.div(
                rx.el.div(
                    input_form(),
                    class_name="w-full md:w-1/3 lg:w-1/4 p-4",
                ),
                rx.el.div(
                    rx.cond(
                        ProjectileState.trajectory_data.length()
                        > 1,
                        trajectory_plot_component(),
                        rx.el.div(
                            rx.el.p(
                                "Enter parameters and click 'Calculate Trajectory' to visualize the path.",
                                class_name="text-gray-600 text-center p-10 text-lg",
                            ),
                            class_name="flex items-center justify-center h-[450px] bg-white rounded-lg shadow-md",
                        ),
                    ),
                    class_name="w-full md:w-2/3 lg:w-3/4 p-4",
                ),
                class_name="flex flex-col md:flex-row",
            ),
            class_name="container mx-auto p-4",
        ),
        on_mount=ProjectileState.calculate_default_trajectory,
        class_name="min-h-screen bg-gradient-to-br from-gray-100 to-slate-200",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css"
    ],
)
app.add_page(index)