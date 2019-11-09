# ransac 算法伪代码

    p = 数据集的所有数据
    n = 模型需要的最少数据
    //根据点与模型的残差 和 errorTolerance的值判定该点是否内点还是外点
    errorTolerance = 根据经验设置容限误差
    k = 最大迭代次数
    t = 根据经验设置内点数量的阀值
    结果模型 ResultModel = 初始化
    for(int i=0; i<k; i++){
        模型M1 = 在集合P中随机选择n+i个数据拟合模型
        内点集合S1 = []
        for(随机数据x in 数据集P){
            数据的残差 error = 计算 (随机数据x 与 模型M1 的残差)
            if(error < errorTolerance ){
                内点集合S1.append(x)
            }
        }
        if( 内点集合S1的元素个数 > 阀值t){
            得到结果模型ResultModel =  模型M1
            break; 
        }
    }
    //到这里就已经得到结果模型了，如果结果模型为空，则当前求模型失败，可能需要重新设置k和t的值了。

