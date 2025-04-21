# CONDITION 1: Run the system with off-the-shelf options
完全default的KITTI和TUM的yaml

# CONDITION 2: Reduce  the  number  of  ORB  features   
修改yaml的ORBextractor.nFeatures (default 2000)  

`
Choose 3 levels of number of features (1500 1000 500) 
`


# CONDITION 3: Turn off the outlier rejection
修改脚本 `Optimizer.cc` 位于：

`
~/COMP0249_24-25_ORB_SLAM2/Source/Libraries/ORB_SLAM2/src
`


``` c++
      if (chi2 > chi2Mono[it]) {
        pFrame->mvbOutlier[idx] = true;
        e->setLevel(1);
        nBad++;
      } else {
        pFrame->mvbOutlier[idx] = false;
        e->setLevel(0);
      }
```

to

``` c++
    pFrame->mvbOutlier[idx] = false;
    e->setLevel(0);
```

# CONDITION 4: Turn off the loop closure
修改脚本 `System.cc`, 取消loop closure线程

``` c++
  // Initialize the Loop Closing thread and launch
  mpLoopCloser = new LoopClosing(mpMap, mpKeyFrameDatabase, mpVocabulary,
                                 mSensor != MONOCULAR);
  mptLoopClosing = new thread(&ORB_SLAM2::LoopClosing::Run, mpLoopCloser);
```
