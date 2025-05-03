import numpy as np
import pickle
import pandas as pd
import os

model_path = os.path.join(os.path.dirname(__file__), "dt_model.pkl")


# Feature names expected by the model
feature_names = [
    'BEDS', 'BATH', 'PROPERTYSQFT', 
    'STATE_10001', 'STATE_10002', 'STATE_10003', 'STATE_10004', 'STATE_10005', 'STATE_10006', 'STATE_10007', 
    'STATE_10009', 'STATE_10010', 'STATE_10011', 'STATE_10012', 'STATE_10013', 'STATE_10014', 'STATE_10016', 
    'STATE_10017', 'STATE_10018', 'STATE_10019', 'STATE_10021', 'STATE_10022', 'STATE_10023', 'STATE_10024', 
    'STATE_10025', 'STATE_10026', 'STATE_10027', 'STATE_10028', 'STATE_10029', 'STATE_10030', 'STATE_10031', 
    'STATE_10032', 'STATE_10033', 'STATE_10034', 'STATE_10035', 'STATE_10036', 'STATE_10037', 'STATE_10038', 
    'STATE_10039', 'STATE_10040', 'STATE_10044', 'STATE_10065', 'STATE_10069', 'STATE_10075', 'STATE_10128', 
    'STATE_10280', 'STATE_10282', 'STATE_10301', 'STATE_10302', 'STATE_10303', 'STATE_10304', 'STATE_10305', 
    'STATE_10306', 'STATE_10307', 'STATE_10308', 'STATE_10309', 'STATE_10310', 'STATE_10312', 'STATE_10314', 
    'STATE_10451', 'STATE_10452', 'STATE_10453', 'STATE_10454', 'STATE_10455', 'STATE_10456', 'STATE_10457', 
    'STATE_10458', 'STATE_10459', 'STATE_10460', 'STATE_10461', 'STATE_10462', 'STATE_10463', 'STATE_10464', 
    'STATE_10465', 'STATE_10466', 'STATE_10467', 'STATE_10468', 'STATE_10469', 'STATE_10470', 'STATE_10471', 
    'STATE_10472', 'STATE_10473', 'STATE_10474', 'STATE_10475', 'STATE_11001', 'STATE_11004', 'STATE_11005', 
    'STATE_11040', 'STATE_11101', 'STATE_11102', 'STATE_11103', 'STATE_11104', 'STATE_11105', 'STATE_11106', 
    'STATE_11109', 'STATE_11201', 'STATE_11203', 'STATE_11204', 'STATE_11205', 'STATE_11206', 'STATE_11207', 
    'STATE_11208', 'STATE_11209', 'STATE_11210', 'STATE_11211', 'STATE_11212', 'STATE_11213', 'STATE_11214', 
    'STATE_11215', 'STATE_11216', 'STATE_11217', 'STATE_11218', 'STATE_11219', 'STATE_11220', 'STATE_11221', 
    'STATE_11222', 'STATE_11223', 'STATE_11224', 'STATE_11225', 'STATE_11226', 'STATE_11228', 'STATE_11229', 
    'STATE_11230', 'STATE_11231', 'STATE_11232', 'STATE_11233', 'STATE_11234', 'STATE_11235', 'STATE_11236', 
    'STATE_11237', 'STATE_11238', 'STATE_11249', 'STATE_11354', 'STATE_11355', 'STATE_11356', 'STATE_11357', 
    'STATE_11358', 'STATE_11360', 'STATE_11361', 'STATE_11362', 'STATE_11363', 'STATE_11364', 'STATE_11365', 
    'STATE_11366', 'STATE_11367', 'STATE_11368', 'STATE_11369', 'STATE_11370', 'STATE_11372', 'STATE_11373', 
    'STATE_11374', 'STATE_11375', 'STATE_11377', 'STATE_11378', 'STATE_11379', 'STATE_11385', 'STATE_11411', 
    'STATE_11412', 'STATE_11413', 'STATE_11414', 'STATE_11415', 'STATE_11416', 'STATE_11417', 'STATE_11418', 
    'STATE_11419', 'STATE_11420', 'STATE_11421', 'STATE_11422', 'STATE_11423', 'STATE_11426', 'STATE_11427', 
    'STATE_11429', 'STATE_11432', 'STATE_11433', 'STATE_11435', 'STATE_11436', 'STATE_11691', 'STATE_11692', 
    'STATE_11693', 'STATE_11694', 'STATE_11697', 'TYPE_Co-op', 'TYPE_Coming', 'TYPE_Condo', 'TYPE_Condop', 
    'TYPE_Contingent', 'TYPE_For', 'TYPE_Foreclosure', 'TYPE_House', 'TYPE_Land', 'TYPE_Mobile', 'TYPE_Multi-family', 
    'TYPE_Pending', 'TYPE_Townhouse'
]


# Main function for model price prediction calls
def predict_with_model(input_data):
    """
    Predict with the trained Decision Tree model.

    Parameters:
        input_data (dict): Dictionary containing input features. 
                          The first three features ('BEDS', 'BATH', 'PROPERTYSQFT') are required (numerical).
                          Additional binary features can be set to True if necessary. Otherwise, they default to False.

    Returns:
        float: Predicted value from the model.
    """
    


    # Initialize the feature array input with zeros, so most of the binary features default to false which should anyway be 0/false
    feature_array = np.zeros(len(feature_names))

    # Ensure the three important/required numerical features are provided
    required_features = ['BEDS', 'BATH', 'PROPERTYSQFT']
    for feature in required_features:
        if feature not in input_data:
            raise ValueError(f"Missing required feature: {feature}")
        # puts the binary feature in the correct position of the model input
        feature_array[feature_names.index(feature)] = input_data[feature]

    # Set the binary features if provided in input_data
    for feature, value in input_data.items():
        if feature in feature_names and feature not in required_features:
            # puts the binary feature in the correct position of the model input
            feature_array[feature_names.index(feature)] = value

    # Convert feature array into required Pandas DataFrame
    feature_df = pd.DataFrame([feature_array], columns=feature_names)

    try:
        # Load the presaved trained model
        with open(model_path, "rb") as file:
            model = pickle.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Model file 'dt_model.pkl' not found. Ensure the model is saved and accessible.")
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the model: {e}")

    # Make prediction
    prediction = round(model.predict(feature_df)[0], 2)
    return prediction# Example usage: