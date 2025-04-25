# CONDITION 1: Run the system with off-the-shelf options
完全default的KITTI和TUM的yaml


# CONDITION 2: Reduce  the  number  of  ORB  features   
修改yaml的 `ORBextractor.nFeatures` (default 2000)  

`
Choose 3 levels of number of features
`

我们选择：(1500 1000 500)   
TUM default 1000, (750 500 200)

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

改成：（不判断是否是离群点 全部接受）

``` c++
    pFrame->mvbOutlier[idx] = false;
    e->setLevel(0);
```

# CONDITION 4: Turn off the loop closure
见这个[issue](https://github.com/raulmur/ORB_SLAM2/issues/256#issuecomment-513260613)  

# 命名规则
`result_*data*_*FeaturePointNumber*_*ifOutlier*_*ifLoop*`

eg: result_KITTI_1500_1_0.txt
    result_TUM_2000_0_0.txt (default)
    result_TUM_1000_0_1.txt


# 分个活：一共2x4x2x2种
## Part 1:
qzw：KITTI
wyk：TUM

## Part 2:
jyy：对于自己的数据集，保证slam效果的同时，如何downsample，减小colmap的时间


# Evaluation_EVO:

1. 运行 `eval_tum_batch.sh`，保存结果为pdf，保存数据为zip

2. 运行如下脚本提取zip里的error数据 保存为csv

``` sh
evo_res evo_eval/office/*_RPE_ANGLE.zip \
  --save_table evo_eval/office_RPE_ANGLE_summary.csv \
  --use_filenames
```

(RPE, RPE_ANGLE同理)