import numpy as np


class Trajectory:
    def __init__(self, states, actions, costs):
        self.states = np.squeeze(states.numpy())
        self.actions = np.squeeze(actions.numpy())
        self.costs = np.squeeze(costs.numpy())

    @property
    def initial_state(self):
        return self.states[0]

    @property
    def final_state(self):
        return self.states[-1]

    @property
    def total_cost(self):
        return np.sum(self.costs)

    @property
    def cumulative_cost(self):
        return np.cumsum(self.costs)

    @property
    def cost_to_go(self):
        return np.cumsum(self.costs[::-1])[::-1]

    def __len__(self):
        return len(self.actions)

    def __getitem__(self, t):
        return (self.states[t + 1], self.actions[t], self.costs[t])

    def __repr__(self):
        init = self.initial_state
        final = self.final_state
        total = self.total_cost
        return f"Trajectory(init={init}, final={final}, total={total:.4f})"

    def __str__(self):
        rows = [("Steps", "States", "Actions", "Costs")]
        for t, (state, action, cost) in enumerate(self):
            step = str(t)
            state = ", ".join([f"{x:8.4f}" for x in state])
            state = f"[{state}]"
            action = ", ".join([f"{u:8.4f}" for u in action])
            action = f"[{action}]"
            cost = f"{cost:8.4f}"
            rows.append((step, state, action, cost))

        cols = list(zip(*rows))
        sizes = [max(map(len, col)) for col in cols]

        rslt = " | ".join(h.center(sz) for h, sz in zip(rows[0], sizes)) + "\n"
        rslt += " | ".join("=" * sz for sz in sizes) + "\n"
        for transition in rows[1:]:
            transition = (col.center(sz) for col, sz in zip(transition, sizes))
            transition = " | ".join(transition)
            rslt += transition + "\n"
        return rslt
