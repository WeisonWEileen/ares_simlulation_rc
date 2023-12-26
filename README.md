<h1>Sustech ARES RC2024 Simulation</h1>
<p>本项目使用麦克纳姆轮小车,搭配mid360和nDof机械臂,对全自动机器人R2进行仿真,完成小球夹取</p>
<p>效果预览</p>
<img src="https://github.com/WeisonWEileen/ares_simlulation_rc/raw/master/docs/preview.png" alt="picture" title="gazebo仿真与rviz显示">

<p>目前包尚未包括fastlio,livox,icp,自行安装</p>
<html>
 
    cd colcon_ws/src #进入你的工作空间的src目录
    mkdir rc && cd rc
    git clone https://github.com/WeisonWEileen/ares_simlulation_rc.git
    cd colcon_ws      
    colcon build --symlink-build

</html>
<p>使用方法</p>
<html>

    ./letsgo.sh
    
</html>