# IPython

from IPython.display import display
import sympy as sym

def cosines(J, K, M, Jp, Kp, Mp):

    result = sym.zeros(3, 3)

    if Jp == J - 1: 
    
        fJ = 4*J*sym.sqrt(4*J**2 - 1)
        
        fKz = -2*sym.sqrt(J**2 - K**2) if Kp == K else 0
        fKy = +sym.sqrt((J+K)*(J+K-1)) if Kp == K - 1 else \
              -sym.sqrt((J-K)*(J-K-1)) if Kp == K + 1 else 0
        fKx = -sym.sqrt((J-K)*(J-K-1))/(-sym.I) if Kp == K + 1 else \
              +sym.sqrt((J+K)*(J+K-1))/(+sym.I) if Kp == K - 1 else 0
        
        fMY = +sym.sqrt((J+M)*(J+M-1)) if Mp == M - 1 else \
              -sym.sqrt((J-M)*(J-M-1)) if Mp == M + 1 else 0
        fMX = -sym.sqrt((J-M)*(J-M-1))/(+sym.I) if Mp == M + 1 else \
              +sym.sqrt((J+M)*(J+M-1))/(-sym.I) if Mp == M - 1 else 0
        fMZ = -2*sym.sqrt(J**2 - M**2) if Mp == M else 0
         
        
    elif Jp == J:
        
        # not yet implemented
        pass
        
    elif Jp == J + 1:
        
        fJ =  4*(J + 1)*sym.sqrt((2*J + 1)*(2*J + 3))
        
        fKz = 2*sym.sqrt((J + 1)**2 - K**2) if Kp == K else 0
        fKy = +sym.sqrt((J-K+1)*(J-K+2))if Kp == K - 1 else \
              -sym.sqrt((J+K+1)*(J+K+2)) if Kp == K + 1 else 0
        fKx = -sym.sqrt((J+K+1)*(J+K+2))/(-sym.I) if Kp == K + 1 else \
              +sym.sqrt((J-K+1)*(J-K+2))/(+sym.I) if Kp == K - 1 else 0
        
        fMY = +sym.sqrt((J-M+1)*(J-M+2)) if Mp == M - 1 else \
              -sym.sqrt((J+M+1)*(J+M+2)) if Mp == M + 1 else 0
        fMX = -sym.sqrt((J+M+1)*(J+M+2))/(+sym.I) if Mp == M + 1 else \
              +sym.sqrt((J-M+1)*(J-M+2))/(-sym.I) if Mp == M - 1 else 0
        fMZ = 2*sym.sqrt((J + 1)**2 - M**2) if Mp == M else 0
        
    result[0, 0] = fKx * fMX / fJ   # Xx
    result[1, 0] = fKy * fMX / fJ   # Xy
    result[2, 0] = fKz * fMX / fJ   # Xz
    result[0, 1] = fKx * fMY / fJ   # Yx
    result[1, 1] = fKy * fMY / fJ   # Yy
    result[2, 1] = fKz * fMY / fJ   # Yz
    result[0, 2] = fKx * fMZ / fJ   # Zx
    result[1, 2] = fKy * fMZ / fJ   # Zy
    result[2, 2] = fKz * fMZ / fJ   # Zz
    
    return result


if __name__ == '__main__':
    
    # example: symmetric top with z dipole moment
    mu = sym.Matrix([0, 0, 1]).T
    
    J, K, M = sym.symbols('J K M')
    
    c_same = cosines(J, K, M, J + 1, K, M)
    c_plus = cosines(J, K, M, J + 1, K, M + 1)
    c_mins = cosines(J, K, M, J + 1, K, M - 1)
    
    mu_z    = (mu*c_same)[2]
    mu_mins = (mu*c_mins)[1] - sym.I*(mu*c_mins)[0]
    mu_plus = (mu*c_plus)[1] + sym.I*(mu*c_plus)[0]    
    
    result = mu_z**2 + (mu_mins**2 + mu_plus**2)/2
    
    display(sym.factor(sym.simplify(result)))
    print('J -> J + 1')
    
    c_same = cosines(J, K, M, J - 1, K, M)
    c_plus = cosines(J, K, M, J - 1, K, M + 1)
    c_mins = cosines(J, K, M, J - 1, K, M - 1)
    
    mu_z    = (mu*c_same)[2]
    mu_mins = (mu*c_mins)[1] - sym.I*(mu*c_mins)[0]
    mu_plus = (mu*c_plus)[1] + sym.I*(mu*c_plus)[0]    
    
    result = mu_z**2 + (mu_mins**2 + mu_plus**2)/2
    
    display(sym.factor(sym.simplify(result)))
    print('J -> J - 1')
    
    
