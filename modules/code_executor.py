def execute_code(code, df):

    local_vars = {"df": df}

    exec(code, {}, local_vars)

    return local_vars.get("result")