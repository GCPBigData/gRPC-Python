import os
import lib

if __name__ == '__main__':
    client = lib.FileClient('localhost:8888')

    # demo for file uploading
    in_file_name = 'C:/teste/file2.parquet'
    print("FAZENDO UPLOADING DO ARQUIVO PARQUET")
    client.upload(in_file_name)

    #demo for file downloading:
    out_file_name = 'C:/teste/file2.parquet'
    if os.path.exists(out_file_name):
       print("aqui 1")
       os.remove(out_file_name)
       print("aqui 2")
    client.download('file.paquet', out_file_name)
    print("aqui 3")
    os.system(f'sha1sum {in_file_name}')
    os.system(f'sha1sum{out_file_name}')
    print("aqui 4")