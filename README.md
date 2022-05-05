# orbslam-deblur-pkg
A ROS Package which deblurs images for ORB-SLAM 2. This is part of a main repository that can be found here: [Main Repo](https://github.com/Prassi07/orb-slam-16833). This is the implementation of the project part of the course 16-833 Robot Localization and Mapping. It aims to implement ORBSLAM 2 on legged and wheeled robotic platform.

This repository implements a custom deblur algorthm to extend ORBSLAM 2 to deal with motion blur introduced by fast moving robot platforms. It uses a laplacian transform with a threshold set manually to determine if an input frame is blurred or not. If blurred, those frames are smoothened using a gaussian blur to remove noise and then sharpened. This sharpened frame is then inputted to ORBSLAM for feature extraction.

This algorithm helps ensure the robot does not lose localization even when moving at high speeds.  
