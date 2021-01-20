import argparse
import os
import datetime, time
from utility import read_list_homo_sapiens_genes, check_gene_and_alias, get_gene_info_from_name
import subprocess as sb
from draw import draw_from_filter


print("----- START FILTER -----")

start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--gtarget', help='Target gene used to filter the data', required=True)
args = parser.parse_args()

target_lists = args.gtarget.split(',')
# print(target_lists)

filepath = os.path.join(os.getcwd(), 'export_data', 'df_resulted.csv')

for target in target_lists:
    filterdir_path = os.path.join(os.getcwd(), 'export_data', f'{target}_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
    os.makedirs(filterdir_path)
    filename = os.path.join(filterdir_path, 'df_filtered.csv')

    list_all_genes = read_list_homo_sapiens_genes()

    gene_info_target = get_gene_info_from_name(target, list_all_genes)
    # print(gene_info_target)

    gene_target = check_gene_and_alias(target, gene_info_target[1])

    try:
        sb.check_output(f'grep -wE \'{gene_target}|{gene_info_target[0]}\' {filepath} > {filename}', shell=True)
    except sb.CalledProcessError as e:
        print('The filter did not find any results!')
        exit()

    draw_from_filter(filterdir_path)

print("----- END FILTER -----")
m, s = divmod(time.time() - start_time, 60)
print(f"----- DONE EXECUTION ({round(m)} mins, {round(s)} secs) -----")