#!/usr/bin/env python3
import os
import sys
import argparse
import signal
import time
import serial, serial.tools.list_ports
import csv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class Stats:
    num_measurements: int
    min_delay: float
    max_delay: float
    mean_delay: float
    median_delay: float
    std_dev: float



def parse_arguments():
    parser = argparse.ArgumentParser(
        description="This script obtains delay measurements from a Glass-to-Glass device connected via USB, "
        "saves results and statistics to a CSV file, and displays the results in a histogram plot. "
        "You can also use it to display results from saved measurements in a previous test, in which case "
        "the CSV file is read from rather than written to."
    )
    parser.add_argument(
        "filename",
        nargs="?",
        default="results.csv",
        type=Path,
        help="The name of the CSV file where the data is saved. It is also the name for the saved plot. "
        "Default is 'results.csv' which will cause 'results.png' to be created as well. "
        "This is the filename used when using the '--readcsv' option as well.",
    )
    parser.add_argument(
        "-num_measurements",
        "-n",
        nargs="?",
        default=100,
        type=int,
        help="An integer for the number of measurements to save and use when generating statistics. Default is 100.",
    )
    parser.add_argument(
        "-threshold_offset",
        "-t",
        nargs="?",
        default=10,
        type=int,
        help="The threshold for distinguishing between light and dark.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="The script won't print the measurements to the terminal (but will still save them into the CSV file).",
    )
    parser.add_argument(
        "--readcsv",
        "-r",
        action="store_true",
        help="Reads a previously generated CSV and plots it. "
        "Be sure to provide the name of the CSV file if it's not the default name.",
    )
    parser.add_argument(
        "--calibrate",
        "-c",
        action="store_true",
        default=True,
        help="Calibrate sensor before running measurements."
        "This will check the sensor values for when the led is on and off, and set the threshold thereafter",
    )
    parser.add_argument(
        "--light_time",
        "-l",
        nargs="?",
        default=0,
        type=float,
        help="The time in seconds the light is on. 0 means until stopped",
    )

    args = parser.parse_args()
    if args.filename.suffix != ".csv":
        print("Error: Provided filename is invalid or does not have .csv extension")
        sys.exit(1)
    return args


def find_arduino_on_serial_port() -> serial.Serial:
    devices = serial.tools.list_ports.comports()
    for device in devices:
        if device.manufacturer is not None:
            if "Arduino" in device.manufacturer:
                print(f"Found Arduino at {device[0]}")
                return serial.Serial(device[0], 115200, timeout=10)

    raise ConnectionRefusedError("Did not find Arduino on any serial port. Is it connected?")



def read_measurements_from_arduino(serial: serial.Serial, args) -> List[float]:
    num_measurements = args.num_measurements
    quiet_mode = args.quiet

    print(f"Collecting {num_measurements} measurements from the Arduino")
    if quiet_mode:
        print("Running in quiet mode, won't print the measurements to the terminal")

    initMeasurement(serial, num_measurements)

    # Read messages from Arduino
    timeout = time.time() + 0.01
    while True:
        a = serial.readline().decode()
        if time.time() > timeout:
            break

    measurements = []
    i = 0
    overall_rounds = 0
    init_message = 0

    try: 
        while i < num_measurements:
            overall_rounds += 1
            a = serial.readline().decode()
            if "." in a:
                init_message = 1
                i += 1
                a = a.replace("\n", "")
                a = a.replace("\r", "")
                measurements.append(float(a))
                append_measurement_to_csv(args.filename, [a])
                if not quiet_mode:
                    print(f"[{i}/{num_measurements}]: {a} ms")
            else:
                if overall_rounds > 0 and init_message == 1:
                    print(
                        "Did not receive msmt data from the Arduino for another 5 seconds. "
                        "Is the phototransistor still sensing the LED?"
                    )
                else:
                    print(
                        """Did not receive msmt data from the Arduino for 5 seconds.
    Is the LED showing up on the screen?
    Is the phototransistor pointing towards the screen?
    Is the screen brightness high enough (max recommended)?"""
                    )
                    init_message = 1
    except KeyboardInterrupt:
        print("Process interrupted by user, returning to main menu...")
        time.sleep(2)

    return measurements


def write_measurements_to_csv(csv_file: Path, measurements: List[float], stats: Stats) -> None:
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Samples", "Min", "Max", "Mean", "Median", "stdDev"])
        writer.writerow(
            [
                stats.num_measurements,
                stats.min_delay,
                stats.max_delay,
                stats.mean_delay,
                stats.median_delay,
                stats.std_dev,
            ]
        )
        writer.writerow(measurements)

    print(f"Saved results to {csv_file}")

def write_measurements_to_csv(csv_file: Path, measurements: List[float]) -> None:
    with open(csv_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["latency"])
        for measurement in measurements:
            writer.writerow([measurement])

    print(f"Saved results to {csv_file}")
    
def append_measurement_to_csv(csv_file: Path, measurements: List[float]) -> None:
    with open(csv_file, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["latency"])
        for measurement in measurements:
            writer.writerow([measurement])


def read_measurements_from_csv(csv_file: Path):
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 0:  # header row, do nothing
                pass
            elif i == 1:  # stats values
                stats = Stats(*(float(i) for i in row))
            elif i == 2:  # measurement samples
                measurements = [float(i) for i in row]
                break  # ignore further rows
    print(f"Obtained values from {csv_file}")

    return measurements, stats


def generate_stats(measurements: List[float]) -> Stats:
    measurements_np = np.array(measurements)

    min_delay = np.min(measurements_np)
    max_delay = np.max(measurements_np)
    mean_delay = np.mean(measurements_np)
    median_delay = np.median(measurements_np)
    std_dev = np.std(measurements_np)

    stats = Stats(len(measurements_np), min_delay, max_delay, mean_delay, median_delay, std_dev)

    print(f"\nmin: {min_delay:.2f} ms | max: {max_delay:.2f} ms | median: {median_delay:.2f} ms")
    print(f"mean: {mean_delay:.2f} ms | std_dev: {std_dev:.2f} ms\n")

    return stats


def plot_results(measurements: List[float], stats: Stats, png_file: Path) -> None:
    
    # Histogram
    fig_h = plt.figure()
    ax_h = fig_h.add_subplot(211)
    
    ax_h.hist(measurements, bins=20) 
    fig_h.canvas.manager.set_window_title(png_file.name)
    ax_h.set_title("Latency Histogram")
    ax_h.set_xlabel("Latency (ms)")
    ax_h.set_ylabel("Frequency")
    
    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
    textstr1 = "\n".join(
        (
            r"$\mathrm{min}=%.2f$" % (stats.min_delay,),
            r"$\mathrm{max}=%.2f$" % (stats.max_delay,),
            r"$\mathrm{median}=%.2f$" % (stats.median_delay,),
        )
    )
    # place it at position x=0.05, y=0.95, relative to the top and left of the box
    ax_h.text(
        0.05,
        0.95,
        textstr1,
        transform=ax_h.transAxes,
        fontsize=14,
        verticalalignment="top",
        horizontalalignment="left",
        bbox=props,
    )
    textstr2 = "\n".join((r"$\mu=%.2f$" % (stats.mean_delay,), r"$\sigma=%.2f$" % (stats.std_dev,)))
    # place it at position x=0.95, y=0.90, relative to the top and right of the box
    ax_h.text(
        0.95,
        0.95,
        textstr2,
        transform=ax_h.transAxes,
        fontsize=14,
        verticalalignment="top",
        horizontalalignment="right",
        bbox=props,
    )

  
    # Linear plot
    ax_l = fig_h.add_subplot(212)

    x_range = range(len(measurements))
    ax_l.plot(x_range, measurements, marker='o') 
    ax_l.set_title("Linear plot")
    ax_l.set_xlabel("Sample")
    ax_l.set_ylabel("Latency (ms)")

    plt.show()


def write_to_serial(serial: serial.Serial, data):
    # print(f"Writing to serial: {data}")
    serial.write(data.encode())
    time.sleep(0.05)
    #response = serial.readline().decode().rstrip('\r\n')
    #print("Done calibrating. Results:")     
    #print(response + "\n")


def calibrate(serial: serial.Serial, threshold_offset: int):
    write_to_serial(serial, "cali")
    _ = serial.readline().decode().rstrip('\r\n') 
    # print(_)
    write_to_serial(serial, str(threshold_offset))
    response = serial.readline().decode().rstrip('\r\n')
    #_ = serial.readline().decode().rstrip('\r\n')
    print("Done calibrating. Results:")     
    print(response + "\n")

def test_light(serial: serial.Serial, seconds: float):
    write_to_serial(serial, "light_on")
    _ = serial.readline().decode().rstrip('\r\n')
    
    try:
        if seconds < 0.0001:      
            while True:
                measurement = serial.readline().decode().rstrip('\r\n')
                print(measurement)
        else:
            start_time = time.time()
            while time.time() - start_time < seconds:
                measurement = serial.readline().decode().rstrip('\r\n')
                print(measurement)
    except KeyboardInterrupt:
        pass
    finally:
        write_to_serial(serial, "light_off")
        print("Done testing light.")
        print("Turning off light (3s)")
        time.sleep(3)

    

def initMeasurement(serial: serial.Serial, numMeasurement):
    write_to_serial(serial, "meas")
    _ = serial.readline().decode().rstrip('\r\n')
    write_to_serial(serial, str(numMeasurement))

def clear():
    os.system("clear") if os.name == "posix" else os.system("cls")

def print_main_menu():
    clear()
    print("********************************************")
    print("*       Glass to glass measuring tool      *")
    print("********************************************")
    print("*                                          *")
    print("*     [1] Start measuring                  *")
    print("*     [2] Read from CSV                    *")
    print("*     [3] Setup                            *")
    print("*     [4] Test light (Alpha)               *")
    print("*     [5] Calibrate                        *")
    print("*     [0] Exit                             *")
    print("*                                          *")
    print("********************************************")
    print("Please enter your choice:")
    
def print_setup_menu():
    clear()
    print("********************************************")
    print("*                Setup                     *")
    print("********************************************")
    print("*                                          *")
    print("*     [1] Change number of measurements    *")
    print("*     [2] Change threshold offset          *")
    print("*     [3] Set quiet mode                   *")
    print("*     [4] Change filename                  *")
    print("*     [5] Toggle calibration before meas.  *")
    print("*     [6] Back                             *")
    print("*                                          *")
    print("********************************************")
    print("Please enter your choice:")
    
def print_calibration_menu():
    clear()
    print("********************************************")
    print("*                Calibration               *")
    print("********************************************")
    print("*                                          *")
    print("*     [1] Calibrate before meas. ON        *")
    print("*     [2] Calibrate before meas. OFF       *")
    print("*     [3] Back                             *")
    print("*                                          *")
    print("********************************************")
    print("Please enter your choice:")
    
def print_quiet_menu():
    clear()
    print("********************************************")
    print("*                Quiet mode                *")
    print("********************************************")
    print("*                                          *")
    print("*     [1] Set quiet mode ON                *")
    print("*     [2] Set quiet mode OFF               *")
    print("*     [3] Back                             *")
    print("*                                          *")
    print("********************************************")
    print("Please enter your choice:")



def menu(args):
    
    while True:
        try:
            print_main_menu()
            choice = input()

            if choice == "1":
                serial = find_arduino_on_serial_port()
                print("Warmup serial (3 sec)")
                time.sleep(3)

                if args.calibrate:
                    print("\nCalibrating")
                    calibrate(serial, args.threshold_offset)

                g2g_delays = read_measurements_from_arduino(serial, args)
                serial.close()

                stats = generate_stats(g2g_delays)
                try:
                    write_measurements_to_csv(args.filename, g2g_delays) # , stats)
                except:
                    print(g2g_delays)

                plot_results(g2g_delays, stats, args.filename.with_suffix(".png"))

            elif choice == "2":
                filename = input("Enter the name of the CSV file: ")
                g2g_delays, stats = read_measurements_from_csv(filename)
                plot_results(g2g_delays, stats, filename.with_suffix(".png"))

            elif choice == "3":
                while True:
                    print_setup_menu()
                    choice = input()
                    
                    if choice == "1":
                        print("Current number of measurements is", args.num_measurements)
                        args.num_measurements = int(input("Enter new number of measurements: "))
                        break
                    elif choice == "2":
                        print("Current threshold offset is", args.threshold_offset)
                        args.threshold_offset = int(input("Enter new threshold offset: "))
                        break
                    elif choice == "3":
                        
                        while True:
                            print_quiet_menu()
                            print("Current quiet mode is", args.quiet)
                            choice = input()
                            if choice == "1":
                                args.quiet = True
                                break
                            elif choice == "2":
                                args.quiet = False
                                break
                            elif choice == "3":
                                break
                            else:
                                print("Invalid choice. Please try again.")
                        break                     
                    elif choice == "4":
                        clear()
                        print("Current filename is", args.filename)
                        args.filename = Path(input("Enter new filename: "))
                        break
                    elif choice == "5":
                        while True:
                            print_calibration_menu()
                            print("Current calibration mode is", args.calibrate)
                            choice = input()
                            if choice == "1":
                                args.calibrate = True
                                break
                            elif choice == "2":
                                args.calibrate = False
                                break
                            elif choice == "3":
                                break
                            else:
                                print("Invalid choice. Please try again.")
                        break
                    elif choice == "6":
                        break
                        
            elif choice == "4":
                serial = find_arduino_on_serial_port()
                print("Warmup serial (3 sec)")
                time.sleep(3)

                write_to_serial(serial, "test_light")
                _ = serial.readline().decode().rstrip('\r\n')
                try:
                    test_light(serial, args.light_time)
                except Exception as e:
                    print(f"Error: {e}")
                    print("Failed to test light")

                write_to_serial(serial, "stop")
                serial.close()
                time.sleep(2)
                
            elif choice == "5":
                serial = find_arduino_on_serial_port()
                print("Warmup serial (3 sec)")
                time.sleep(3)

                if args.calibrate:
                    print("\nCalibrating")
                    calibrate(serial, args.threshold_offset)

                write_to_serial(serial, "stop")
                serial.close()
                time.sleep(2)
                
            elif choice == "0":
                print("Exiting...")
                sys.exit(0)

            else:
                print("Invalid choice. Please try again.")
    
        except ConnectionRefusedError as e:
            print(f'ConnectionRefusedError: {e}')
            print("Try again in 5 seconds...")
            time.sleep(5)
                    
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Trying again in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Exiting...")
            time.sleep(5)
            break


def main() -> None:
    args = parse_arguments()
    
    menu(args)

if __name__ == "__main__":
    main()
