from __init__ import *

k_vector = ()
lambda_vector = ()
h_bar, c, k_b = constants.hbar, constants.speed_of_light, constants.Boltzmann


def main(N=1):
    with open(os.path.join(DATA_DIR, "config.json"),'r') as infile:
        config = json.load(infile)

    global k_vector, lambda_vector

    lambda_vector = np.linspace(config['lambda_min'], config['lambda_max'], config['lambda_N'])
    OPD_vector = np.flip(np.linspace(config['OPD_min'], config['OPD_max'], config['OPD_N']))
    OPD_vector = [np.random.normal(OPD, config['OPD_err']) for OPD in OPD_vector]
    #print(OPD_vector)
    k_vector = 2*pi/lambda_vector
    T = np.random.normal(3000.0, 200, N)

    output = np.array([Add_Noise(Michaelson_Intereferometer_Action(Generate_White_Light(T), OPD), scale=1e-3) for OPD in OPD_vector])
    print("Observation Made!")
    return output


def Generate_White_Light(Temp: float):
    global k_vector

    """
    Generate a white light spectrum from a tungsten-halogen lamp, according to Planck's Law.
    """
    planck_func = lambda k: h_bar*(c**2)*(k**3)/(4*pi**3)*1/(np.exp(h_bar*c*k/(k_b*Temp))-1)
    output_spectrum = planck_func(k_vector)

    return output_spectrum

def Michaelson_Intereferometer_Action(input_spectrum: np.ndarray, OPD: float):
    global lambda_vector
    """
    Transform the input spectrum (Intensity) via the action of a Michaelson Interferometer of optical path difference 
    wrt the laser wavelength as OPD
    """

    mic_func = lambda I, k: 4*I*(np.cos(k*OPD/2)**2)
    input_tmp = np.column_stack((input_spectrum, lambda_vector))
    output_spectrum = [mic_func(I, 2*pi/lambda_point) for [I, lambda_point] in input_tmp]

    return output_spectrum

def Add_Noise(input_spectrum, scale):
    """
    Adds Random Noise paramterized via scale to the input spectrum. Noise is generated via a
    normal distribution in k-space, with average intensity scale times total intensity of the
    spectrum.
    """
    
    intensity_avg = np.average(input_spectrum)
    noise_avg = intensity_avg * scale
    noise_vector = noise_avg * np.random.chisquare(df=3, size=len(input_spectrum))
    return input_spectrum + noise_vector

    





