import numpy as np
import matplotlib.pyplot as plt
from operator import attrgetter


class ParetoVisualScreen:

    def __init__(self):
        # self.graphSize = v2(1, 1)
        plt.ion()
        plt.figure(figsize=(8, 8))
        self.ax = plt.gca()
        self.ax.set_autoscale_on(True)

    def Update(self, pool, generation):
        x_list = []
        y_list = []
        x_pareto = []
        y_pareto = []
        #  X axis
        minSupervisorsFitness = min(pool, key=attrgetter('SupervisorsFitness'))\
            .SupervisorsFitness
        maxSupervisorsFitness = max(pool, key=attrgetter('SupervisorsFitness'))\
            .SupervisorsFitness
        diffSupervisorsFitness = maxSupervisorsFitness - minSupervisorsFitness

        # Y axis

        minStudentsFitness = min(pool, key=attrgetter('NormalizedStudentsFitness')).NormalizedStudentsFitness
        maxStudentsFitness = max(pool, key=attrgetter('NormalizedStudentsFitness')).NormalizedStudentsFitness
        diffStudentsFitness = maxStudentsFitness - minStudentsFitness

        for i in range(len(pool)):
            individual = pool[i]

            x = individual.SupervisorsFitness
            y = individual.StudentsFitness

            if individual.Rank == 1:
                x_pareto.append(x)
                y_pareto.append(y)
            else:
                x_list.append(x)
                y_list.append(y)

        pos_pareto_x = np.array(x_pareto)
        pos_pareto_y = np.array(y_pareto)
        positions_x = np.array(x_list)
        positions_y = np.array(y_list)

        # plt.plot(positions_y, positions_x, '.', pos_pareto_y, pos_pareto_x, '*')
        lines, = self.ax.plot([], [], '.')
        # pareto_line, = self.ax.plot([], [])
        pareto_line, = self.ax.plot([], [], '*', color="red")
        pareto_line.set_xdata(pos_pareto_x)
        pareto_line.set_ydata(pos_pareto_y)
        lines.set_xdata(positions_x)
        lines.set_ydata(positions_y)

        self.ax.relim()
        self.ax.autoscale_view(True,True,True)
        plt.xlabel('SupervisorsFitness')
        plt.ylabel('StudentsFitness')
        #We need to draw *and* flush
        # self.figure.canvas.draw()
        # self.figure.canvas.flush_events()
        # plt.text(900, 60, generation, fontsize = 22)
        # plt.draw()
        for x,y in zip(pos_pareto_x, pos_pareto_y):
            plt.text(x, y, (x, y))
        plt.show()
        plt.pause(0.1)
        plt.cla()


