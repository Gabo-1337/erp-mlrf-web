def validate_float(value):
    # * Validates a float value, used in 
    value = str(value) or ""
    try:
        float_value = float(value)
        if 0.01 <= float_value <= 1.00:
            return True
        else:
            return False
    except ValueError:
        return False

def validate_integer(value):
    # * validates an integer, used in number_project_cpf_input
    # * Validates a integer value within a range, used in time_spend_company_cpf_input
    value = str(value) or ""
    try:
        if value.isdigit() and 1 <= int(value) <= 10:
            return True
        else:
            return False
    except ValueError:
        return False

def validate_amh_range(value):
    # * Validates a float value within a range, used in average_monthly_hours_cpf_input
    value = str(value) or ""
    try:
        if value.isdigit() and 1 <= int(value) <= 310:
            return True
        else:
            return False
    except ValueError:
        return False

