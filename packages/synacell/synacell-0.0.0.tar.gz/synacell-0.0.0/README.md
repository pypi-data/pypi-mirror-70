# SynaCell

Synapses and cells.

Spiking neural network (SNN) consisted of cells with processing algorithms, connected by synapses with realistic signal transmission properties. The engine that runs the SNN is written in plain C++ with interface in Python, for simplicity and platform mobility.

## Usefull commands

### How to make Microsoft Visual Studio project from CMakeLists.txt

By running the following command from the folder where CMakeLists.txt lies, you can make a .sln project files and use it in Visual Studio IDE:

```
cmake -G "Visual Studio 15 2017" -A x64
```
