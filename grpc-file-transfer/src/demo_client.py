import os
import lib

if __name__ == '__main__':
    client = lib.FileClient('localhost:8888')

    # demo for file uploading
    #in_file_name = 'C:/teste/file2.parquet'
    #print("FAZENDO UPLOADING DO ARQUIVO PARQUET")
    #client.upload(in_file_name)

    #demo for file downloading:
    out_file_name = 'D:/teste/baixado/file.mkv'
    if os.path.exists(out_file_name):
       os.remove(out_file_name)

    print(client)
    client.download('file.mkv', out_file_name)
    #os.system(f'sha1sum {in_file_name}')
    #os.system(out_file_name)
    print("ARQUIVO BAIXADO NA PASTA :", out_file_name)