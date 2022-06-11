import os

for int_year in range(2014,2023):
    os.chdir( str(int_year) )
    for int_month in range(1,13):
        str_dir = f'{int_month:0>2d}'
        if os.path.exists(str_dir):
            os.chdir( str_dir )
            str_txt = ''
            for int_day in range(31,0,-1):
                str_read = f'{int_year}{int_month:0>2d}{int_day:0>2d}.txt'
                print(str_read)
                if os.path.isfile(str_read):
                    str_txt += open( str_read, 'r' ).read() + '\n\n'
            str_write = f'{int_year}{int_month:0>2d}.tex'
            os.chdir('..')
            print(str_write)
            open(str_write, 'w').write(str_txt)
    os.chdir('..')
