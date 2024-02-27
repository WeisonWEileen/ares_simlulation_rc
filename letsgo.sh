cd ../..

cmds=(
    "ros2 launch rc_map rc_simulation.launch.py \
        use_sim_time:=true"
    
	"ros2 launch imu_complementary_filter complementary_filter.launch.py \
		use_sim_time:=true
    "
	"ros2 launch fast_lio mapping_mid360.launch.py \
        use_sim_time:=true rviz:=false
    "
	"ros2 launch linefit_ground_segmentation_ros segmentation.launch.py
        use_sim_time:=true" 
    "
    ros2 launch pointcloud_to_laserscan pointcloud_to_laserscan_launch.py
        use_sim_time:=true"
    # "
    # ros2 launch icp_localization_ros2 bringup.launch.py
    #     use_sim_time:=true"
    "
    ros2 launch rm_navigation online_async_launch.py \
    use_sim_time:=true
	"
    "ros2 launch rm_navigation bringup_no_amcl_launch.py \
		use_sim_time:=true
	" 
)

for cmd in "${cmds[@]}"
do 
    echo Current CMD : "$cmd"
    gnome-terminal -- bash -c "cd $(pwd);source install/setup.bash;$cmd;exec bash;"
    sleep 0.2
done


# cartographer 建图ros2 launch rc_cartographer.launch use_sim_time:=True
#启动键盘控制  
    # "ros2 run teleop_twist_keyboard teleop_twist_keyboard"
