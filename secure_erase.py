import os
import shutil
import sys

def get_free_space(directory):
    total, used, free = shutil.disk_usage(directory)
    return free

def print_progress_bar(iteration, total, remaining_gb, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {remaining_gb:.2f} GB remaining {suffix}', end='\r')
    if iteration == total:
        print()

def fill_drive(directory, passes=1):
    file_path = os.path.join(directory, 'filler.dat')
    
    for pass_num in range(1, passes + 1):
        print(f"Pass {pass_num}/{passes}")

        free_space = get_free_space(directory)
        size_in_bytes = free_space - 4096  # leave a small buffer for system reservations

        with open(file_path, 'wb') as f:
            # Choose the pattern based on the pass number
            if pass_num % 3 == 1:
                pattern = b'\x00'
            elif pass_num % 3 == 2:
                pattern = b'\xFF'
            else:
                pattern = os.urandom(1)

            pattern_size = len(pattern)
            total_written = 0
            # Calculate total steps for the progress bar based on 1MB blocks
            total_steps = size_in_bytes // (1024 * 1024)  # 1MB blocks

            for step in range(total_steps):
                # Write 1MB blocks to the file
                f.write(pattern * (1024 * 1024 // pattern_size))
                total_written += 1024 * 1024
                # Calculate remaining GB
                remaining_gb = (size_in_bytes - total_written) / (1024 * 1024 * 1024)
                # Update the progress bar
                print_progress_bar(step + 1, total_steps, remaining_gb, prefix='Progress:', suffix='Complete', length=50)

            # Write any remaining bytes if size_in_bytes is not a multiple of 1MB
            remaining_bytes = size_in_bytes - total_written
            if remaining_bytes > 0:
                f.write(pattern * (remaining_bytes // pattern_size))
                total_written += remaining_bytes
                # Update the remaining GB for the final write
                remaining_gb = (size_in_bytes - total_written) / (1024 * 1024 * 1024)

            # Ensure the progress bar reaches 100%
            print_progress_bar(total_steps, total_steps, remaining_gb, prefix='Progress:', suffix='Complete', length=50)
            print(f"\nWritten {total_written} bytes.")

        # Remove the file after writing is complete
        os.remove(file_path)
        print(f"Deleted file {file_path}.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <directory> [passes]")
        sys.exit(1)

    target_directory = sys.argv[1]
    passes = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    fill_drive(target_directory, passes)
    print("Drive filling complete.")