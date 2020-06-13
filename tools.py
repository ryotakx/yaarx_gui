import subprocess


def compute(program_name, *param):
    run = subprocess.Popen(
        './' + program_name,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    for i in param:
        run.stdin.write(i + '\n')
    run.stdin.close()

    output = [str(line) for line in run.stdout]
    print(output)
    return_list = output[-2].strip().split('=')
    if len(return_list) == 2:
        return_list.append('')
    return return_list


def conversion(inputs):
    output = []
    for param in inputs:
        if param[0] == 'decimal':
            output.append(hex(int(param[1]))[2:])
        elif param[0] == 'binary':
            output.append(hex(int(param[1], 2))[2:])
        else:
            output.append(param[1])
    return output
