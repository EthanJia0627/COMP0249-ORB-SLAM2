# COMP0249 Coursework 2  

**Group 2**  
Yukai Wang, Yiyang Jia, Zewen Qu  
MSc Robotics and Artificial Intelligence,  
Department of Computer Science,  
University College London

**Contact Emails**:  
yukai.wang.24@ucl.ac.uk  
yiyang.jia.24@ucl.ac.uk  
zewen.qu.24@ucl.ac.uk


# CONDITION code Modification
For specific changes below, slease see this [commit](https://github.com/EthanJia0627/COMP0249_24-25_ORB_SLAM2/commit/ef84de2af54bb124a8b3b9d4eaf129de246b6a32) of this [repo](https://github.com/EthanJia0627/COMP0249_24-25_ORB_SLAM2). 

## CONDITION 1: Run the system with off-the-shelf options
Completely default KITTI and TUM yaml files.

## CONDITION 2: Reduce the number of ORB features
Modify the `ORBextractor.nFeatures` in the yaml file.  

### KITTI Dataset
- Default: 2000  
- 3 Levels:  
  - 1750 
  - 1500
  - 1250  

### TUM Dataset
- Default: 1000  
- 3 Levels:  
  - 850  
  - 700  
  - 550  

## CONDITION 3: Turn off the outlier rejection
Modify the script `Optimizer.cc` located at:

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

Change to: (accept all outliers)

``` c++
    pFrame->mvbOutlier[idx] = false;
    e->setLevel(0);
```

## CONDITION 4: Turn off the loop closure
Comment out all loop closure related threads in `System.cc`, `LocalMapping.cc` and  `Tracking.cc`.  
Reference: see this [issue](https://github.com/raulmur/ORB_SLAM2/issues/256#issuecomment-513260613).

# Result File Name
`result_*data*_*FeaturePointNumber*_*ifOutlier*_*ifLoop*`

e.g.: result_KITTI_1500_1_0.txt  
  result_TUM_2000_0_0.txt (default)  
  result_TUM_1000_0_1.txt

# EVO:

1. Run `eval_tum_batch.sh`, save the result iamge sas a PDF, and save the data as a ZIP file.

2. Run the following script to extract error data from the ZIP file and save it as a CSV:

``` sh
evo_res evo_eval/office/*_RPE_ANGLE.zip \
  --save_table evo_eval/office_RPE_ANGLE_summary.csv \
  --use_filenames
```

(similar to RPE, RPE_ANGLE)
