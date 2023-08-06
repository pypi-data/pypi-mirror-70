from meteva.base import *
from meteva.method import *
from meteva.product.program.fun import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def score(sta_ob_and_fos0,method,s = None,g = None,gll = None,para1 = None,para2 = None,plot = "line",show = False,excel_path = None):

    if s is not None:
        if g is not None:
            if g == "last_range" or g == "last_step":
                s["drop_last"] = False
            else:
                s["drop_last"] = True
    sta_ob_and_fos = sele_by_dict(sta_ob_and_fos0, s)

    if type(method) == str:
        method =  globals().get(method)
    if method == meteva.method.FSS_time:
        if g == "dtime":
            print("FSS_time 检验时，参数group_by不能选择dtime")
            return
    sta_ob_and_fos_list,group_list_list1 = group(sta_ob_and_fos,g,gll)
    data_name = meteva.base.get_stadata_names(sta_ob_and_fos)
    fo_num = len(data_name) -1
    ensemble_score_method = [meteva.method.cr]
    group_num = len(sta_ob_and_fos_list)

    if para1 is None:
        para_num = 1
    else:
        para_name_list = []
        mutil_list = [meteva.method.ts_multi,meteva.method.bias_multi,meteva.method.ets_multi,
                      meteva.method.mr_multi,meteva.method.far_multi]
        if method in mutil_list:
            para_num = len(para1)+1
            para_name_list = ["<" +  str(para1[0])]
            for i in range(len(para1)-1):
                para_name_list.append("["+str(para1[i]) + ","+str(para1[i+1])+")")
            para_name_list.append(">=" + str(para1[-1]))

        else:
            para_num = len(para1)
            for i in range(len(para1)):
                para_name_list.append(para1[i])

    sta_result = None

    if method == meteva.method.FSS_time:
        #统计dtime的集合
        dtime_list = list(set(sta_ob_and_fos["dtime"].values.tolist()))
        dtime_list.sort()
        ndtime = len(dtime_list)
        result= []
        for sta_ob_and_fo in sta_ob_and_fos_list:
            # 将观测和预报数据重新整理成FSS_time所需格式
            ob = in_member_list(sta_ob_and_fo,[data_name[0]])
            ob_dtimes = None
            for k in range(ndtime):
                dtimek = dtime_list[k]
                sta_obk = in_dtime_list(ob,[dtimek])
                set_stadata_names(sta_obk,[data_name[0]+ str(dtimek)])
                ob_dtimes = combine_on_leve_time_id(ob_dtimes,sta_obk)
            result1 = []
            #print(ob_dtimes)
            ob_array = ob_dtimes.values[:,6:]
            for j in range(fo_num):
                fo = in_member_list(sta_ob_and_fo, [data_name[j+1]])
                fo_dtimes = None
                for k in range(ndtime):
                    dtimek = dtime_list[k]
                    sta_fok = in_dtime_list(fo, [dtimek])
                    set_stadata_names(sta_fok, [data_name[j+1] + str(dtimek)])
                    fo_dtimes = combine_on_leve_time_id(fo_dtimes, sta_fok)
                fo_array = fo_dtimes.values[:,6:]

                #调用检验程序
                if para1 is None:
                    para1 = [1e-30]
                result2 = FSS_time(ob_array, fo_array, para1, para2)
                result1.append(result2)
            result.append(result1)
        result = np.array(result) #将数据转换成数组
        result = result.squeeze()

    else:
        nead_lon_lat = False
        if g == "id" and gll is None:
            nead_lon_lat = True
        lon_lat_list = []

        if method in ensemble_score_method:
            result = np.zeros((group_num,para_num))
            for i in range(group_num):
                sta = sta_ob_and_fos_list[i]
                #if(len(sta.index) == 0):
                #    result[i,:] = meteva.base.IV
                #else:
                ob = sta[data_name[0]].values
                fo = sta[data_name[1:]].values
                if para1 is None:
                    result[i, :] = method(ob, fo)
                else:
                    result[i,:] = method(ob, fo,para1)
                if nead_lon_lat:
                    lon_lat_list.append(sta.iloc[0,[4,5]])
        else:
            if fo_num ==0:
                result = np.zeros((group_num,para_num))
            else:
                result = np.zeros((group_num,fo_num,para_num))
            for i in range(group_num):
                #print(group_num)
                sta = sta_ob_and_fos_list[i]
                #if(len(sta.index) == 0):
                #    result[i,:] = meteva.base.IV
                #else:
                ob = sta[data_name[0]].values
                if fo_num>0:
                    for j in range(fo_num):
                        fo = sta[data_name[j+1]].values
                        if para1 is None:
                            result[i, j] = method(ob, fo)
                        else:
                            result[i,j] = method(ob, fo,para1)
                else:
                    if para1 is None:
                        result[i] = method(ob, None)
                    else:
                        result[i] = method(ob, None,para1)
                if nead_lon_lat:
                    lon_lat_list.append(sta.iloc[0,[4,5]])

        # 将结果输出到excel
        if excel_path is not None:
            meteva.base.creat_path(excel_path)
            if fo_num ==0:
                fo_num = 1
            result.reshape([group_num,fo_num,para_num])
            group_dict ={"group":group_list_list1}
            model_dict = {"member":data_name[1:]}
            para_dict = {"threshold":para_name_list}
            name_dict_list = [group_dict,model_dict,para_dict]
            meteva.base.write_array_to_excel(result,excel_path,name_dict_list)

        result = result.squeeze()
        if nead_lon_lat:
            df = pd.DataFrame(lon_lat_list)
            df["id"] = group_list_list1
            df["level"] = np.NAN
            df["time"] = np.NAN
            df["dtime"] = np.NAN
            if fo_num ==0:
                if para1 is None:
                    df["ob"] = result
                else:
                    if isinstance(para1,list):
                        for i in range(len(para1)):
                            para = para1[i]
                            df[para] = result[:,i]
                    else:
                        df[para1] = result
            else:
                result = result.reshape(group_num,fo_num,para_num)
                for j in range(fo_num):
                    if para1 is None:
                        df[data_name[1+j]] = result[:,j,0]
                    else:
                        if isinstance(para1, list):
                            for i in range(len(para1)):
                                para = para1[i]
                                df[data_name[1+j]+"_"+str(para)] = result[:,j, i]
                        else:
                            df[data_name[1 + j]] = result[:,j,0]

            sta_result = sta_data(df)
    if show:
        if plot == "line":
            if g == "dtime":
                x = np.arange(len(group_list_list1))
                plt.plot(result,label = data_name[1])
                plt.xticks(x,group_list_list1)
                plt.xlabel("预报时效")
                plt.ylabel("ME")
                plt.legend()
                plt.show()



    return result,group_list_list1,sta_result



def score_id_scatter(sta_ob_and_fos0,method,s = None,g = None,gll = None,group_list_list = None,para1 = None,para2 = None,save_dir = None,save_path = None,title = None):
    pass


def score_id_contourf(sta_ob_and_fos0,method,s = None,g = None,gll = None,group_list_list = None,para1 = None,para2 = None,save_dir = None,save_path = None,title = None):
    pass


def score_time_dtime_line():
    pass

def score_time_dtime_mesh():
    pass