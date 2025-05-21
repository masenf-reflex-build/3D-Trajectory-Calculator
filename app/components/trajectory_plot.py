import reflex as rx
from app.state import ProjectileState


def trajectory_plot_component() -> rx.Component:
    return rx.el.div(
        rx.recharts.scatter_chart(
            rx.recharts.cartesian_grid(
                stroke_dasharray="3 3", stroke="#cccccc"
            ),
            rx.recharts.x_axis(
                rx.recharts.label(
                    value="Distance (m)",
                    position="insideBottom",
                    dy=10,
                    fill="#374151",
                ),
                type="number",
                data_key="x",
                domain=["auto", "auto"],
                allow_data_overflow=True,
                stroke="#4b5563",
            ),
            rx.recharts.y_axis(
                rx.recharts.label(
                    value="Height (m)",
                    angle=-90,
                    position="insideLeft",
                    dx=-5,
                    fill="#374151",
                ),
                type="number",
                data_key="y",
                domain=[0, "auto"],
                allow_data_overflow=True,
                stroke="#4b5563",
            ),
            rx.recharts.scatter(
                data_key="y",
                name="Trajectory",
                fill="#4f46e5",
                line=True,
                shape="circle",
            ),
            rx.recharts.tooltip(
                cursor={"strokeDasharray": "3 3"}
            ),
            rx.recharts.legend(
                wrapper_style={"paddingTop": "10px"}
            ),
            data=ProjectileState.trajectory_data,
            height=450,
            margin={
                "left": 20,
                "right": 20,
                "top": 25,
                "bottom": 20,
            },
            class_name="bg-white p-4 rounded-lg shadow-md w-full",
        ),
        rx.el.div(
            rx.el.h3(
                "Trajectory Metrics",
                class_name="text-xl font-semibold mt-6 mb-3 text-gray-800",
            ),
            rx.el.div(
                rx.el.p(
                    f"Max Height: {ProjectileState.max_height_str} m",
                    class_name="text-md text-gray-700 py-1",
                ),
                rx.el.p(
                    f"Total Range: {ProjectileState.total_range_str} m",
                    class_name="text-md text-gray-700 py-1",
                ),
                rx.el.p(
                    f"Time of Flight: {ProjectileState.time_of_flight_str} s",
                    class_name="text-md text-gray-700 py-1",
                ),
                class_name="mt-4 p-4 bg-gray-100 rounded-lg shadow-sm",
            ),
            class_name="w-full",
        ),
        rx.cond(
            ProjectileState.error_message != "",
            rx.el.div(
                ProjectileState.error_message,
                class_name="mt-4 p-3 bg-red-100 text-red-700 border border-red-300 rounded-md shadow-sm",
            ),
            rx.fragment(),
        ),
        class_name="w-full",
    )