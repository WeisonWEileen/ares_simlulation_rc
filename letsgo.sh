cd ../..
cmds=("ros2 launch rc_map rc_simulation.launch.py"
	"ros2 launch linefit_ground_segmentation_ros segmentation.launch.py" 
	"ros2 launch fast_lio mapping_mid360.launch.py rviz:=true"
    "ros2 run teleop_twist_keyboard teleop_twist_keyboard"
    "ros2 launch pointcloud_to_laserscan pointcloud_to_laserscan_launch.py")

for cmd in "${cmds[@]}"
do 
    echo Current CMD : "$cmd"
    gnome-terminal -- bash -c "cd $(pwd);source install/setup.bash;$cmd;exec bash;"
    sleep 0.2
done