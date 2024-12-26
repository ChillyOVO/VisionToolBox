import scipy
import numpy as np
import src.PDDTVisionToolBox as pd


# 旋转变换
def RotationTransform(Input, formatIn, formatOut):
    """
    旋转变换，角度均使用弧度制
    :param Input: 均采用Numpy 矩阵进行输入，格式为(3,3)的旋转矩阵，或者(1,3)的旋转向量，或者(1,4)的四元数，或者(1,3)的欧拉角
    :param formatIn: 输入类型 V-Vector 旋转向量，M-Matrix 旋转矩阵, Q-Quaternion 四元数, E-Euler 欧拉角
    :param formatOut: 输出类型 V-Vector 旋转向量，M-Matrix 旋转矩阵, Q-Quaternion 四元数, E-Euler 欧拉角
    :return:
    """
    # 拼写矫正
    formatIn = formatIn.upper()
    formatOut = formatOut.upper()
    # 检查输入
    if type(Input) != np.ndarray:
        print("[Input Error] :Input must be a numpy array !")
        return None
    if formatIn == 'V':
        if np.shape(Input) != (3, 1):
            print("[Input Error] :Input must be a (3,1) numpy array !")
            return None
    elif formatIn == 'M':
        if np.shape(Input) != (3, 3):
            print("[Input Error] :Input must be a (3,3) numpy array !")
            return None
    elif formatIn == 'Q':
        if np.shape(Input) != (1, 4):
            print("[Input Error] :Input must be a (1,4) numpy array !")
            return None
    elif formatIn == 'E':
        if np.shape(Input) != (1, 3):
            print("[Input Error] :Input must be a (1,3) numpy array !")
            return None
    else:
        print("[Input Error] :Input format must be V, M, Q or E !")
        return None
    if formatOut != 'V' and formatOut != 'M' and formatOut != 'Q' and formatOut != 'E':
        print("[Input Error] :Output format must be V, M, Q or E !")
        return None

    # 进行变换
    if formatIn == 'V':
        # 旋转向量输入矫正，常规理解旋转向量为3行1列，但实际函数调用时，只接受1行3列类型
        Input = Input.T
        if formatOut == 'M':
            return scipy.spatial.transform.Rotation.from_rotvec(Input).as_matrix()
        elif formatOut == 'Q':
            return scipy.spatial.transform.Rotation.from_rotvec(Input).as_quat()
        elif formatOut == 'E':
            return scipy.spatial.transform.Rotation.from_rotvec(Input).as_euler('zyx')
    elif formatIn == 'M':
        if formatOut == 'V':
            return scipy.spatial.transform.Rotation.from_matrix(Input).as_rotvec()
        elif formatOut == 'Q':
            return scipy.spatial.transform.Rotation.from_matrix(Input).as_quat()
        elif formatOut == 'E':
            return scipy.spatial.transform.Rotation.from_matrix(Input).as_euler('zyx')
    elif formatIn == 'Q':
        if formatOut == 'V':
            return scipy.spatial.transform.Rotation.from_quat(Input).as_rotvec()
        elif formatOut == 'M':
            return scipy.spatial.transform.Rotation.from_quat(Input).as_matrix()
        elif formatOut == 'E':
            return scipy.spatial.transform.Rotation.from_quat(Input).as_euler('zyx')
    elif formatIn == 'E':
        # 欧拉角输入矫正，采用了numpy输入导致无法识别为，角度
        if formatOut == 'V':
            return scipy.spatial.transform.Rotation.from_euler('zyx', Input).as_rotvec()
        elif formatOut == 'M':
            return scipy.spatial.transform.Rotation.from_euler('zyx', Input).as_matrix()
        elif formatOut == 'Q':
            return scipy.spatial.transform.Rotation.from_euler('zyx', Input).as_quat()

    print("[Input Error] :No Necessary to Transform !")
    return None


if __name__ == '__main__':
    mat = np.array([[1, 0, 0],
                    [0, 1, 0],
                    [0, 0, 1]])
    vec = np.array([[1], [1], [1]])
    eul = np.array([[1, 2, 3]])
    qua = np.array([[1, 0, 0, 0]])
    ret = pd.RotationTransform(mat, 'm', 'v')
    print(ret)
