import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch.conditions import UnlessCondition


def generate_launch_description():

    is_sim_arg = DeclareLaunchArgument(
        "is_sim",
        default_value="True"
    )

    is_sim = LaunchConfiguration("is_sim")

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(
                    get_package_share_directory("arduinobot_description"),
                    "urdf",
                    "arduinobot.urdf.xacro",
                )," is_sim:=False"
            ]
        ),
        value_type=str,
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}],
        condition=UnlessCondition(is_sim),
    )

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description,
            "use_sim_time": is_sim},
            os.path.join(
                get_package_share_directory("arduinobot_controller"),
                "config",
                "arduinobot_controllers.yaml",
            ),
        ],
        condition=UnlessCondition(is_sim),
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ],
    )

    head_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["head_controller",
                   "--controller-manager", "/controller_manager"],
    )

    arm_right_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_right_controller",
                   "--controller-manager", "/controller_manager"],
    )

    gripper_rh_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_rh_controller",
                   "--controller-manager", "/controller_manager"],
    )

    arm_left_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["arm_left_controller",
                   "--controller-manager", "/controller_manager"],
    )

    gripper_lh_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["gripper_lh_controller",
                   "--controller-manager", "/controller_manager"],
    )

    leg_rh_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["leg_rh_controller",
                   "--controller-manager", "/controller_manager"],
    )

    leg_lh_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["leg_lh_controller",
                   "--controller-manager", "/controller_manager"],
    )

    

    return LaunchDescription(
        [   
            is_sim_arg,
            robot_state_publisher,
            controller_manager,
            joint_state_broadcaster_spawner,
            head_controller_spawner,
            arm_right_controller_spawner,
            gripper_rh_controller_spawner,
            arm_left_controller_spawner,
            gripper_lh_controller_spawner,
            leg_rh_controller_spawner,
            leg_lh_controller_spawner,
        ]
    )
