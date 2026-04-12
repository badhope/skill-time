import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import crypto from "crypto";

function rollDice(sides: number, count: number = 1): number[] {
  const results: number[] = [];
  for (let i = 0; i < count; i++) {
    results.push(crypto.randomInt(1, sides + 1));
  }
  return results;
}

function pareto(alpha: number = 1.5, xm: number = 1): number {
  const u = crypto.randomInt(1, 1000000) / 1000000;
  return Math.round(xm * Math.pow(u, -1 / alpha));
}

function levyStable(alpha: number = 1.0, gamma: number = 1.0): number {
  const phi = (crypto.randomInt(1, 1000000) / 1000000 - 0.5) * Math.PI;
  const w = -Math.log(crypto.randomInt(1, 1000000) / 1000000);
  const left = Math.sin(alpha * phi) / Math.pow(Math.cos(phi), 1 / alpha);
  const right = Math.pow(Math.cos(phi * (1 - alpha)) / w, (1 - alpha) / alpha);
  return Math.round(gamma * left * right);
}

function wanderSteps(): number {
  const steps = pareto(1.5, 2);
  return Math.min(Math.max(steps, 1), 15);
}

function semanticJumpDistance(): number {
  return Math.abs(levyStable(1.0, 2.0));
}

function dynamicNoiseLevel(step: number, totalSteps: number): number {
  const phase = (step / totalSteps) * Math.PI;
  const base = 0.15;
  const oscillation = 0.1 * Math.sin(2 * phase);
  const criticalPoint = step === Math.floor(totalSteps / 2) ? 0.2 : 0;
  return base + oscillation + criticalPoint;
}

function generateNeurodynamicSeed() {
  const stepCount = wanderSteps();
  return {
    version: "2.0",
    neurodynamics: true,
    path_seed: rollDice(4)[0],
    format_seed: rollDice(4)[0],
    failure_seed: rollDice(100)[0],
    lane_change_seed: rollDice(20)[0],
    collapse_seed: rollDice(100)[0],
    wander_steps: wanderSteps(),
    semantic_jump: semanticJumpDistance(),
    initial_noise: dynamicNoiseLevel(0, stepCount),
    dmn_activation: crypto.randomInt(30, 70) / 100,
    ecn_activation: crypto.randomInt(30, 70) / 100,
    source: "CSPRNG + heavy-tailed distributions",
    distributions: {
      wander: "Pareto(α=1.5)",
      jump: "Levy(α=1.0)",
      noise: "sinusoidal + critical enhancement"
    },
    timestamp: new Date().toISOString()
  };
}

const server = new Server(
  {
    name: "randomskill-mcp-random",
    version: "2.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "roll_dice",
        description: "Cryptographically secure uniform dice roll (for legacy/compatibility only)",
        inputSchema: {
          type: "object",
          properties: {
            sides: {
              type: "number",
              description: "Number of sides on the die (default: 4)",
              default: 4,
            },
            count: {
              type: "number",
              description: "Number of dice to roll (default: 1)",
              default: 1,
            },
          },
        },
      },
      {
        name: "neurodynamic_seed",
        description: "v2.0 FULL NEURODYNAMIC STATE VECTOR - USE THIS FOR ALL REAL THINKING",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "pareto_sample",
        description: "Sample from Pareto distribution (power law, heavy tailed)",
        inputSchema: {
          type: "object",
          properties: {
            alpha: {
              type: "number",
              description: "Shape parameter (default: 1.5)",
              default: 1.5,
            },
          },
        },
      },
      {
        name: "levy_jump",
        description: "Sample from Levy stable distribution (infinite variance flights)",
        inputSchema: {
          type: "object",
          properties: {
            alpha: {
              type: "number",
              description: "Stability parameter (default: 1.0)",
              default: 1.0,
            },
          },
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "roll_dice": {
      const sides = (args?.sides as number) || 4;
      const count = (args?.count as number) || 1;
      const results = rollDice(sides, count);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              sides,
              count,
              results,
              sum: results.reduce((a, b) => a + b, 0),
              distribution: "uniform",
              source: "cryptographically-secure-csprng",
              note: "WARNING: Uniform is unrealistic for human cognition"
            }, null, 2),
          },
        ],
      };
    }

    case "neurodynamic_seed": {
      const result = generateNeurodynamicSeed();
      const pathNames = ['Creative Divergence', 'Analytical Deconstruction', 
                         'Mind-Wandering', 'Pure Random Surprise'];
      return {
        content: [
          {
            type: "text",
            text: `=== NEURODYNAMIC STATE VECTOR v2.0 ===
${JSON.stringify(result, null, 2)}

📊 COGNITIVE DIAGNOSTICS:
  Path: ${result.path_seed} → ${pathNames[result.path_seed - 1]}
  Format: ${result.format_seed}
  Wander Steps: ${result.wander_steps} (Pareto α=1.5, 90% ≤ 4 steps)
  Semantic Jump: ${result.semantic_jump} (Levy α=1.0)
  Initial Noise: ${(result.initial_noise * 100).toFixed(0)}%
  DMN: ${(result.dmn_activation * 100).toFixed(0)}% ↔ ECN: ${(result.ecn_activation * 100).toFixed(0)}%

💥 SPECIAL EVENTS:
  Minor Failure: ${result.failure_seed <= 30 ? 'YES (30%)' : 'NO'}
  Lane Change: ${result.lane_change_seed <= 2 ? 'YES (10%)' : 'NO'}
  ⚠️  FRAMEWORK COLLAPSE: ${result.collapse_seed <= 5 ? 'YES (5%)' : 'NO'}

✅ THESE VALUES ARE EXOGENOUS.
✅ LLM CANNOT OVERRIDE.
✅ NO TAKE-BACKS.
`,
          },
        ],
      };
    }

    case "pareto_sample": {
      const alpha = (args?.alpha as number) || 1.5;
      const sample = pareto(alpha);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              distribution: `Pareto(alpha=${alpha})`,
              sample,
              interpretation: sample <= 4 ? "typical tail" : "HEAVY TAIL EVENT",
              source: "cryptographically-secure",
              note: "Humans produce heavy tails. LLMs produce exponential tails."
            }, null, 2),
          },
        ],
      };
    }

    case "levy_jump": {
      const alpha = (args?.alpha as number) || 1.0;
      const jump = Math.abs(levyStable(alpha));
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              distribution: `LevyStable(alpha=${alpha})`,
              jump_distance: jump,
              interpretation: jump <= 3 ? "local search" : "LEVY FLIGHT - LONG RANGE JUMP",
              source: "cryptographically-secure",
              note: "This is how nature searches. Albatrosses. Bees. Humans."
            }, null, 2),
          },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("RandomSkill MCP Random Server v2.0 running on stdio");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
