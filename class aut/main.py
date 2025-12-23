from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime, date
import json
import os
import math
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'smart-physics-hub-secret-key')

# Comprehensive Physics Topics Database
physics_topics_database = {
    "mechanics": {
        "title": "Mechanics",
        "icon": "fas fa-cog",
        "color": "primary",
        "description": "Study of motion, forces, and energy in physical systems",
        "subtopics": {
            "kinematics": {
                "title": "Kinematics",
                "description": "Motion without considering forces",
                "formulas": {
                    "v = u + at": "Final velocity = Initial velocity + acceleration × time",
                    "s = ut + ½at²": "Displacement with constant acceleration",
                    "v² = u² + 2as": "Velocity-displacement relationship",
                    "s = (u + v)t/2": "Average velocity formula"
                },
                "examples": [
                    "A car accelerates from 0 to 60 km/h in 10 seconds",
                    "A ball thrown upward reaches maximum height",
                    "Free fall motion under gravity"
                ],
                "applications": ["Vehicle motion", "Projectile motion", "Sports analysis"]
            },
            "dynamics": {
                "title": "Dynamics (Newton's Laws)",
                "description": "Motion with forces considered",
                "formulas": {
                    "F = ma": "Newton's Second Law - Force equals mass times acceleration",
                    "F₁ = -F₂": "Newton's Third Law - Action-reaction pairs",
                    "ΣF = 0": "Newton's First Law - Equilibrium condition",
                    "W = mg": "Weight force"
                },
                "examples": [
                    "Pushing a car requires more force than pushing a bicycle",
                    "When you walk, you push back on the ground",
                    "A book on a table experiences balanced forces"
                ],
                "applications": ["Engineering design", "Vehicle safety", "Sports biomechanics"]
            },
            "work_energy": {
                "title": "Work and Energy",
                "description": "Energy transformations and work done by forces",
                "formulas": {
                    "W = F·d·cosθ": "Work done by a force",
                    "KE = ½mv²": "Kinetic energy",
                    "PE = mgh": "Gravitational potential energy",
                    "PE = ½kx²": "Elastic potential energy",
                    "P = W/t": "Power"
                },
                "examples": [
                    "Lifting a weight stores gravitational potential energy",
                    "A moving car has kinetic energy",
                    "A compressed spring stores elastic potential energy"
                ],
                "applications": ["Power generation", "Vehicle efficiency", "Sports performance"]
            },
            "momentum": {
                "title": "Momentum and Impulse",
                "description": "Conservation of momentum in collisions",
                "formulas": {
                    "p = mv": "Momentum",
                    "J = FΔt": "Impulse",
                    "J = Δp": "Impulse-momentum theorem",
                    "Σp_before = Σp_after": "Conservation of momentum"
                },
                "examples": [
                    "Billiard ball collisions",
                    "Car crash safety systems",
                    "Rocket propulsion"
                ],
                "applications": ["Vehicle safety", "Sports equipment", "Space exploration"]
            }
        }
    },
    "waves": {
        "title": "Waves and Oscillations",
        "icon": "fas fa-wave-square",
        "color": "info",
        "description": "Study of periodic motion and wave phenomena",
        "subtopics": {
            "simple_harmonic_motion": {
                "title": "Simple Harmonic Motion",
                "description": "Periodic motion with restoring force",
                "formulas": {
                    "x = A sin(ωt + φ)": "Displacement in SHM",
                    "v = Aω cos(ωt + φ)": "Velocity in SHM",
                    "a = -Aω² sin(ωt + φ)": "Acceleration in SHM",
                    "T = 2π√(m/k)": "Period of mass-spring system",
                    "T = 2π√(L/g)": "Period of simple pendulum"
                },
                "examples": [
                    "Pendulum clock oscillations",
                    "Mass on a spring",
                    "Vibrating guitar string"
                ],
                "applications": ["Clocks", "Musical instruments", "Seismographs"]
            },
            "wave_properties": {
                "title": "Wave Properties",
                "description": "Characteristics of wave motion",
                "formulas": {
                    "v = fλ": "Wave speed equation",
                    "T = 1/f": "Period and frequency relationship",
                    "y = A sin(kx - ωt)": "Sinusoidal wave equation",
                    "k = 2π/λ": "Wave number",
                    "ω = 2πf": "Angular frequency"
                },
                "examples": [
                    "Sound waves in air (v = 343 m/s)",
                    "Light waves in vacuum (v = 3×10⁸ m/s)",
                    "Water waves on a lake"
                ],
                "applications": ["Communication systems", "Medical imaging", "Seismic studies"]
            },
            "sound": {
                "title": "Sound Waves",
                "description": "Longitudinal pressure waves in media",
                "formulas": {
                    "v = √(B/ρ)": "Speed of sound in medium",
                    "I = P²/(2ρv)": "Sound intensity",
                    "β = 10 log(I/I₀)": "Sound level in decibels",
                    "f' = f(v±v_r)/(v±v_s)": "Doppler effect"
                },
                "examples": [
                    "Echo from a mountain",
                    "Doppler shift of ambulance siren",
                    "Ultrasound medical imaging"
                ],
                "applications": ["Audio systems", "Medical diagnostics", "Sonar navigation"]
            },
            "light": {
                "title": "Light and Optics",
                "description": "Electromagnetic waves and optical phenomena",
                "formulas": {
                    "c = fλ": "Speed of light",
                    "n = c/v": "Refractive index",
                    "n₁sinθ₁ = n₂sinθ₂": "Snell's law",
                    "1/f = 1/u + 1/v": "Lens equation",
                    "m = v/u": "Magnification"
                },
                "examples": [
                    "Rainbow formation by refraction",
                    "Magnifying glass focusing light",
                    "Fiber optic communication"
                ],
                "applications": ["Cameras", "Telescopes", "Laser technology"]
            }
        }
    },
    "thermodynamics": {
        "title": "Heat and Thermodynamics",
        "icon": "fas fa-thermometer-half",
        "color": "danger",
        "description": "Study of heat, temperature, and energy transfer",
        "subtopics": {
            "temperature_heat": {
                "title": "Temperature and Heat",
                "description": "Thermal properties and heat transfer",
                "formulas": {
                    "Q = mcΔT": "Heat capacity",
                    "Q = mL": "Latent heat",
                    "α = ΔL/(L₀ΔT)": "Linear expansion coefficient",
                    "P = kA(ΔT/Δx)": "Heat conduction",
                    "P = σAT⁴": "Stefan-Boltzmann law"
                },
                "examples": [
                    "Water boiling at 100°C",
                    "Ice melting requires latent heat",
                    "Metal rails expanding in summer"
                ],
                "applications": ["HVAC systems", "Cooking", "Industrial processes"]
            },
            "gas_laws": {
                "title": "Gas Laws",
                "description": "Behavior of ideal gases",
                "formulas": {
                    "PV = nRT": "Ideal gas law",
                    "P₁V₁/T₁ = P₂V₂/T₂": "Combined gas law",
                    "PV = constant": "Boyle's law (constant T)",
                    "V/T = constant": "Charles's law (constant P)",
                    "P/T = constant": "Gay-Lussac's law (constant V)"
                },
                "examples": [
                    "Balloon expanding when heated",
                    "Pressure cooker operation",
                    "Car tire pressure changes with temperature"
                ],
                "applications": ["Weather prediction", "Engine design", "Refrigeration"]
            },
            "thermodynamic_processes": {
                "title": "Thermodynamic Processes",
                "description": "Energy transformations in thermal systems",
                "formulas": {
                    "ΔU = Q - W": "First law of thermodynamics",
                    "ΔS ≥ 0": "Second law of thermodynamics",
                    "η = W/Q_h": "Heat engine efficiency",
                    "COP = Q_c/W": "Coefficient of performance",
                    "W = ∫PdV": "Work in thermodynamic process"
                },
                "examples": [
                    "Steam engine converting heat to work",
                    "Refrigerator removing heat from cold space",
                    "Carnot cycle theoretical efficiency"
                ],
                "applications": ["Power plants", "Refrigeration", "Heat pumps"]
            }
        }
    },
    "electricity": {
        "title": "Electricity and Magnetism",
        "icon": "fas fa-bolt",
        "color": "warning",
        "description": "Electric and magnetic phenomena",
        "subtopics": {
            "electrostatics": {
                "title": "Electrostatics",
                "description": "Static electric charges and fields",
                "formulas": {
                    "F = kq₁q₂/r²": "Coulomb's law",
                    "E = F/q": "Electric field strength",
                    "V = kq/r": "Electric potential",
                    "C = Q/V": "Capacitance",
                    "U = ½CV²": "Energy stored in capacitor"
                },
                "examples": [
                    "Lightning formation",
                    "Static electricity on clothes",
                    "Capacitors in electronic circuits"
                ],
                "applications": ["Electronic devices", "Lightning protection", "Photocopiers"]
            },
            "current_electricity": {
                "title": "Current Electricity",
                "description": "Moving charges and electrical circuits",
                "formulas": {
                    "I = Q/t": "Electric current",
                    "V = IR": "Ohm's law",
                    "P = VI = I²R = V²/R": "Electrical power",
                    "R_series = R₁ + R₂ + R₃": "Resistors in series",
                    "1/R_parallel = 1/R₁ + 1/R₂ + 1/R₃": "Resistors in parallel"
                },
                "examples": [
                    "Current flow in household wiring",
                    "LED brightness control with resistors",
                    "Battery powering a flashlight"
                ],
                "applications": ["Electrical circuits", "Power distribution", "Electronic devices"]
            },
            "magnetism": {
                "title": "Magnetism",
                "description": "Magnetic fields and forces",
                "formulas": {
                    "F = qvB sinθ": "Magnetic force on moving charge",
                    "F = BIL sinθ": "Force on current-carrying conductor",
                    "B = μ₀I/(2πr)": "Magnetic field around wire",
                    "Φ = BA cosθ": "Magnetic flux",
                    "ε = -dΦ/dt": "Faraday's law of induction"
                },
                "examples": [
                    "Compass needle aligning with Earth's field",
                    "Electric motor operation",
                    "Generator producing electricity"
                ],
                "applications": ["Electric motors", "Generators", "MRI machines"]
            },
            "electromagnetic_induction": {
                "title": "Electromagnetic Induction",
                "description": "Changing magnetic fields producing electricity",
                "formulas": {
                    "ε = -N(dΦ/dt)": "Faraday's law",
                    "ε = BLv": "Motional EMF",
                    "L = Φ/I": "Self-inductance",
                    "ε = -L(dI/dt)": "Self-induced EMF",
                    "U = ½LI²": "Energy in inductor"
                },
                "examples": [
                    "Transformer changing voltage levels",
                    "Generator in power plant",
                    "Induction cooking"
                ],
                "applications": ["Power generation", "Transformers", "Wireless charging"]
            }
        }
    },
    "modern_physics": {
        "title": "Modern Physics",
        "icon": "fas fa-atom",
        "color": "success",
        "description": "Quantum mechanics and relativity",
        "subtopics": {
            "atomic_structure": {
                "title": "Atomic Structure",
                "description": "Structure of atoms and quantum behavior",
                "formulas": {
                    "E = hf": "Planck's equation",
                    "λ = h/p": "de Broglie wavelength",
                    "E_n = -13.6/n² eV": "Hydrogen energy levels",
                    "ΔE = hf": "Photon energy",
                    "p = E/c": "Photon momentum"
                },
                "examples": [
                    "Hydrogen spectrum lines",
                    "Photoelectric effect",
                    "Electron diffraction patterns"
                ],
                "applications": ["Lasers", "LED technology", "Electron microscopes"]
            },
            "nuclear_physics": {
                "title": "Nuclear Physics",
                "description": "Nuclear reactions and radioactivity",
                "formulas": {
                    "E = mc²": "Mass-energy equivalence",
                    "N = N₀e^(-λt)": "Radioactive decay",
                    "t₁/₂ = ln(2)/λ": "Half-life",
                    "Q = (Δm)c²": "Nuclear reaction energy",
                    "A = λN": "Activity of radioactive sample"
                },
                "examples": [
                    "Carbon-14 dating",
                    "Nuclear power generation",
                    "Medical radioisotopes"
                ],
                "applications": ["Nuclear power", "Medical imaging", "Archaeological dating"]
            },
            "relativity": {
                "title": "Special Relativity",
                "description": "Physics at high speeds",
                "formulas": {
                    "γ = 1/√(1-v²/c²)": "Lorentz factor",
                    "t' = γt": "Time dilation",
                    "L' = L/γ": "Length contraction",
                    "E² = (pc)² + (mc²)²": "Relativistic energy",
                    "p = γmv": "Relativistic momentum"
                },
                "examples": [
                    "GPS satellite time corrections",
                    "Particle accelerator experiments",
                    "Muon lifetime in cosmic rays"
                ],
                "applications": ["GPS systems", "Particle physics", "Astrophysics"]
            }
        }
    },
    "astrophysics": {
        "title": "Astrophysics",
        "icon": "fas fa-globe",
        "color": "secondary",
        "description": "Physics of celestial objects and the universe",
        "subtopics": {
            "gravitation": {
                "title": "Gravitation",
                "description": "Gravitational forces and orbital motion",
                "formulas": {
                    "F = Gm₁m₂/r²": "Newton's law of gravitation",
                    "g = GM/r²": "Gravitational field strength",
                    "v = √(GM/r)": "Orbital velocity",
                    "T² = (4π²/GM)r³": "Kepler's third law",
                    "U = -Gm₁m₂/r": "Gravitational potential energy"
                },
                "examples": [
                    "Moon orbiting Earth",
                    "Satellite communication systems",
                    "Tidal forces from Moon and Sun"
                ],
                "applications": ["Satellite technology", "Space exploration", "Tidal predictions"]
            },
            "stellar_physics": {
                "title": "Stellar Physics",
                "description": "Physics of stars and stellar evolution",
                "formulas": {
                    "L = 4πR²σT⁴": "Stefan-Boltzmann law for stars",
                    "λ_max = b/T": "Wien's displacement law",
                    "M = 4πr²ρ": "Mass distribution in stars",
                    "P = ρkT/(μm_u)": "Ideal gas law in stellar cores",
                    "τ = GM²/(RL)": "Kelvin-Helmholtz timescale"
                },
                "examples": [
                    "Sun's energy from nuclear fusion",
                    "Red giant star expansion",
                    "White dwarf cooling"
                ],
                "applications": ["Solar energy", "Stellar navigation", "Exoplanet detection"]
            },
            "cosmology": {
                "title": "Cosmology",
                "description": "Physics of the universe as a whole",
                "formulas": {
                    "H₀ = v/d": "Hubble's law",
                    "z = Δλ/λ": "Cosmological redshift",
                    "t = 1/H₀": "Hubble time",
                    "Ω = ρ/ρ_c": "Density parameter",
                    "a(t) ∝ t^(2/3)": "Scale factor evolution"
                },
                "examples": [
                    "Expanding universe",
                    "Cosmic microwave background",
                    "Dark matter and dark energy"
                ],
                "applications": ["Cosmological models", "Big Bang theory", "Dark matter research"]
            }
        }
    },
    "fluid_mechanics": {
        "title": "Fluid Mechanics",
        "icon": "fas fa-water",
        "color": "info",
        "description": "Study of fluids in motion and at rest",
        "subtopics": {
            "fluid_statics": {
                "title": "Fluid Statics",
                "description": "Fluids at rest and pressure in fluids",
                "formulas": {
                    "P = ρgh": "Hydrostatic pressure",
                    "P₁ + ρgh₁ = P₂ + ρgh₂": "Pascal's principle",
                    "F_b = ρ_fluid × V_displaced × g": "Buoyant force (Archimedes' principle)",
                    "P = F/A": "Pressure definition",
                    "ΔP = ρgΔh": "Pressure difference in fluid"
                },
                "examples": [
                    "Water pressure in swimming pool",
                    "Hydraulic car lift operation",
                    "Ship floating on water",
                    "Atmospheric pressure measurement"
                ],
                "applications": ["Hydraulic systems", "Ship design", "Submarine operation", "Dam construction"]
            },
            "fluid_dynamics": {
                "title": "Fluid Dynamics",
                "description": "Motion of fluids and flow patterns",
                "formulas": {
                    "A₁v₁ = A₂v₂": "Continuity equation",
                    "P₁ + ½ρv₁² + ρgh₁ = P₂ + ½ρv₂² + ρgh₂": "Bernoulli's equation",
                    "F_d = ½ρv²C_dA": "Drag force",
                    "Re = ρvL/μ": "Reynolds number",
                    "Q = Av": "Flow rate"
                },
                "examples": [
                    "Airplane wing lift generation",
                    "Water flow through pipes",
                    "Wind resistance on vehicles",
                    "Blood flow in arteries"
                ],
                "applications": ["Aircraft design", "Pipeline engineering", "Weather prediction", "Medical devices"]
            },
            "viscosity": {
                "title": "Viscosity and Turbulence",
                "description": "Internal friction in fluids and chaotic flow",
                "formulas": {
                    "F = ηA(dv/dy)": "Viscous force (Newton's law of viscosity)",
                    "v = (ρgr²)/(8η)": "Terminal velocity in viscous medium",
                    "f = 64/Re": "Friction factor for laminar flow",
                    "τ = η(du/dy)": "Shear stress in fluid",
                    "ν = η/ρ": "Kinematic viscosity"
                },
                "examples": [
                    "Honey flowing slowly",
                    "Oil lubrication in engines",
                    "Turbulent flow in rivers",
                    "Smoke patterns in air"
                ],
                "applications": ["Lubrication systems", "Oil industry", "Aerodynamics", "Chemical processing"]
            }
        }
    },
    "solid_mechanics": {
        "title": "Solid Mechanics",
        "icon": "fas fa-cube",
        "color": "dark",
        "description": "Behavior of solid materials under forces",
        "subtopics": {
            "elasticity": {
                "title": "Elasticity",
                "description": "Deformation and recovery of materials",
                "formulas": {
                    "σ = F/A": "Stress",
                    "ε = ΔL/L₀": "Strain",
                    "σ = Eε": "Hooke's law (Young's modulus)",
                    "U = ½σε × Volume": "Elastic potential energy",
                    "ν = -ε_lateral/ε_axial": "Poisson's ratio"
                },
                "examples": [
                    "Rubber band stretching",
                    "Steel beam bending",
                    "Spring compression",
                    "Building foundation settlement"
                ],
                "applications": ["Structural engineering", "Material testing", "Bridge design", "Earthquake engineering"]
            },
            "strength_of_materials": {
                "title": "Strength of Materials",
                "description": "Material failure and safety factors",
                "formulas": {
                    "σ_max = Mc/I": "Bending stress",
                    "τ = VQ/(Ib)": "Shear stress in beams",
                    "σ_cr = π²EI/(KL)²": "Euler buckling stress",
                    "SF = σ_ultimate/σ_working": "Safety factor",
                    "K_t = σ_max/σ_nominal": "Stress concentration factor"
                },
                "examples": [
                    "Bridge beam design",
                    "Column buckling failure",
                    "Pressure vessel design",
                    "Aircraft wing structure"
                ],
                "applications": ["Civil engineering", "Mechanical design", "Aerospace engineering", "Safety analysis"]
            },
            "fracture_mechanics": {
                "title": "Fracture Mechanics",
                "description": "Crack propagation and material failure",
                "formulas": {
                    "K_I = σ√(πa)": "Stress intensity factor",
                    "G = K²/E": "Energy release rate",
                    "da/dN = C(ΔK)^m": "Paris law for fatigue crack growth",
                    "J = ∫W dy": "J-integral",
                    "σ_f = K_Ic/√(πa)": "Fracture stress"
                },
                "examples": [
                    "Crack in airplane fuselage",
                    "Fatigue failure in bridges",
                    "Glass breaking patterns",
                    "Metal fatigue in engines"
                ],
                "applications": ["Failure analysis", "Material selection", "Structural integrity", "Quality control"]
            }
        }
    },
    "plasma_physics": {
        "title": "Plasma Physics",
        "icon": "fas fa-fire",
        "color": "danger",
        "description": "Fourth state of matter - ionized gases",
        "subtopics": {
            "plasma_fundamentals": {
                "title": "Plasma Fundamentals",
                "description": "Basic properties of plasma state",
                "formulas": {
                    "ω_p = √(ne²/(ε₀m))": "Plasma frequency",
                    "λ_D = √(ε₀kT/(ne²))": "Debye length",
                    "β = nkT/(B²/2μ₀)": "Plasma beta",
                    "ν_c = ne⁴ln(Λ)/(12π³/²ε₀²m^(1/2)(kT)^(3/2))": "Collision frequency",
                    "Γ = e²/(4πε₀akT)": "Plasma parameter"
                },
                "examples": [
                    "Lightning plasma channel",
                    "Fluorescent light operation",
                    "Solar corona",
                    "Plasma TV display"
                ],
                "applications": ["Fusion energy", "Plasma displays", "Space propulsion", "Material processing"]
            },
            "magnetohydrodynamics": {
                "title": "Magnetohydrodynamics (MHD)",
                "description": "Plasma behavior in magnetic fields",
                "formulas": {
                    "J = σ(E + v × B)": "Ohm's law in plasma",
                    "∂B/∂t = ∇ × (v × B) + η∇²B": "Magnetic diffusion equation",
                    "v_A = B/√(μ₀ρ)": "Alfvén wave speed",
                    "R_m = μ₀σvL": "Magnetic Reynolds number",
                    "F = J × B": "Lorentz force density"
                },
                "examples": [
                    "Solar wind interaction with Earth's magnetosphere",
                    "Tokamak plasma confinement",
                    "Stellar magnetic fields",
                    "Plasma propulsion systems"
                ],
                "applications": ["Fusion reactors", "Space weather prediction", "Astrophysical modeling", "Plasma thrusters"]
            },
            "fusion_physics": {
                "title": "Nuclear Fusion in Plasmas",
                "description": "Controlled nuclear fusion reactions",
                "formulas": {
                    "⟨σv⟩ = ∫σ(v)vf(v)dv": "Reaction rate coefficient",
                    "P_fusion = n₁n₂⟨σv⟩E_fusion": "Fusion power density",
                    "nτT > 10²¹ m⁻³skeV": "Lawson criterion",
                    "Q = P_fusion/P_input": "Fusion gain factor",
                    "τ_E = W/P_loss": "Energy confinement time"
                },
                "examples": [
                    "ITER tokamak project",
                    "Inertial confinement fusion",
                    "Stellar nucleosynthesis",
                    "Hydrogen bomb reactions"
                ],
                "applications": ["Clean energy generation", "Space propulsion", "Medical isotope production", "Neutron sources"]
            }
        }
    },
    "biophysics": {
        "title": "Biophysics",
        "icon": "fas fa-dna",
        "color": "success",
        "description": "Physics principles applied to biological systems",
        "subtopics": {
            "biomechanics": {
                "title": "Biomechanics",
                "description": "Mechanical principles in living organisms",
                "formulas": {
                    "F = kx": "Bone elasticity (Hooke's law)",
                    "P = ρgh + P₀": "Blood pressure",
                    "v = √(2gh)": "Blood flow velocity",
                    "τ = ηγ̇": "Viscous stress in blood",
                    "E = σ/ε": "Elastic modulus of tissues"
                },
                "examples": [
                    "Bone fracture mechanics",
                    "Heart pumping mechanism",
                    "Muscle contraction forces",
                    "Joint movement analysis"
                ],
                "applications": ["Prosthetic design", "Sports medicine", "Rehabilitation engineering", "Surgical planning"]
            },
            "membrane_physics": {
                "title": "Cell Membrane Physics",
                "description": "Physical properties of biological membranes",
                "formulas": {
                    "V = RT/F × ln(C_out/C_in)": "Nernst equation",
                    "I = gV": "Ohm's law for ion channels",
                    "J = -D(dc/dx)": "Fick's law of diffusion",
                    "ΔG = RTln(C₂/C₁)": "Free energy of transport",
                    "τ = RC": "Membrane time constant"
                },
                "examples": [
                    "Nerve impulse propagation",
                    "Ion channel function",
                    "Cell membrane potential",
                    "Drug transport across membranes"
                ],
                "applications": ["Drug delivery", "Neuroscience research", "Bioelectronics", "Medical diagnostics"]
            },
            "molecular_biophysics": {
                "title": "Molecular Biophysics",
                "description": "Physics of biological molecules",
                "formulas": {
                    "ΔG = ΔH - TΔS": "Gibbs free energy",
                    "k = Ae^(-E_a/RT)": "Arrhenius equation for enzyme kinetics",
                    "F = kT/p × ∂ln(Z)/∂x": "Molecular force",
                    "D = kT/(6πηr)": "Stokes-Einstein relation",
                    "K_d = [A][B]/[AB]": "Dissociation constant"
                },
                "examples": [
                    "Protein folding dynamics",
                    "DNA double helix stability",
                    "Enzyme-substrate binding",
                    "Molecular motor function"
                ],
                "applications": ["Drug design", "Protein engineering", "Genetic therapy", "Molecular diagnostics"]
            }
        }
    },
    "geophysics": {
        "title": "Geophysics",
        "icon": "fas fa-mountain",
        "color": "warning",
        "description": "Physics of Earth and planetary systems",
        "subtopics": {
            "seismology": {
                "title": "Seismology",
                "description": "Study of earthquakes and seismic waves",
                "formulas": {
                    "v_p = √((K + 4μ/3)/ρ)": "P-wave velocity",
                    "v_s = √(μ/ρ)": "S-wave velocity",
                    "M = log₁₀(A) + 3log₁₀(Δ) - 2.92": "Richter magnitude",
                    "E = 10^(1.5M + 4.8)": "Seismic energy",
                    "Δt = d/v": "Travel time"
                },
                "examples": [
                    "Earthquake wave propagation",
                    "Tsunami generation",
                    "Building seismic response",
                    "Oil exploration seismics"
                ],
                "applications": ["Earthquake prediction", "Building codes", "Oil exploration", "Nuclear monitoring"]
            },
            "gravity_and_magnetism": {
                "title": "Earth's Gravity and Magnetism",
                "description": "Gravitational and magnetic fields of Earth",
                "formulas": {
                    "g = GM/r²": "Gravitational acceleration",
                    "Δg = -2πGρt": "Bouguer anomaly",
                    "B = μ₀M/(4πr³)": "Magnetic dipole field",
                    "F = qv × B": "Magnetic force on charged particle",
                    "∇²V = -4πGρ": "Poisson's equation for gravity"
                },
                "examples": [
                    "GPS satellite corrections",
                    "Magnetic compass navigation",
                    "Aurora formation",
                    "Mineral exploration surveys"
                ],
                "applications": ["Navigation systems", "Mineral exploration", "Space weather", "Archaeological surveys"]
            },
            "atmospheric_physics": {
                "title": "Atmospheric Physics",
                "description": "Physics of Earth's atmosphere",
                "formulas": {
                    "P = P₀e^(-mgh/kT)": "Barometric formula",
                    "dT/dz = -g/c_p": "Adiabatic lapse rate",
                    "f = 2Ωsin(φ)": "Coriolis parameter",
                    "τ = I₀e^(-τ)": "Beer's law for atmospheric absorption",
                    "v_g = (1/f) × (∂P/∂y, -∂P/∂x)": "Geostrophic wind"
                },
                "examples": [
                    "Weather pattern formation",
                    "Greenhouse effect",
                    "Ozone layer depletion",
                    "Climate change mechanisms"
                ],
                "applications": ["Weather forecasting", "Climate modeling", "Air pollution control", "Renewable energy"]
            }
        }
    },
    "medical_physics": {
        "title": "Medical Physics",
        "icon": "fas fa-heartbeat",
        "color": "danger",
        "description": "Physics applications in medicine and healthcare",
        "subtopics": {
            "medical_imaging": {
                "title": "Medical Imaging Physics",
                "description": "Physics principles behind medical imaging",
                "formulas": {
                    "I = I₀e^(-μx)": "X-ray attenuation",
                    "f_D = 2f₀v cos(θ)/c": "Doppler ultrasound frequency",
                    "T₁ = ln(2)/λ": "MRI T1 relaxation time",
                    "SNR ∝ √(N × t)": "Signal-to-noise ratio",
                    "λ = h/p": "de Broglie wavelength for electron microscopy"
                },
                "examples": [
                    "X-ray chest imaging",
                    "Ultrasound pregnancy scans",
                    "MRI brain imaging",
                    "CT scan reconstruction"
                ],
                "applications": ["Diagnostic radiology", "Nuclear medicine", "Radiation therapy", "Medical research"]
            },
            "radiation_therapy": {
                "title": "Radiation Therapy Physics",
                "description": "Physics of cancer treatment with radiation",
                "formulas": {
                    "D = E/m": "Absorbed dose",
                    "H = D × w_R": "Equivalent dose",
                    "E = D × w_T": "Effective dose",
                    "N = N₀e^(-λt)": "Radioactive decay",
                    "I = I₀e^(-μx)": "Radiation attenuation"
                },
                "examples": [
                    "Linear accelerator treatment",
                    "Brachytherapy implants",
                    "Proton beam therapy",
                    "Gamma knife surgery"
                ],
                "applications": ["Cancer treatment", "Radiation safety", "Treatment planning", "Quality assurance"]
            },
            "biomedical_optics": {
                "title": "Biomedical Optics",
                "description": "Light interaction with biological tissues",
                "formulas": {
                    "I = I₀e^(-μt)": "Beer-Lambert law",
                    "μ_s' = μ_s(1-g)": "Reduced scattering coefficient",
                    "δ = 1/√(3μ_a(μ_a + μ_s'))": "Optical penetration depth",
                    "R = (n₁-n₂)²/(n₁+n₂)²": "Fresnel reflection",
                    "λ_max = b/T": "Wien's law for thermal imaging"
                },
                "examples": [
                    "Pulse oximetry monitoring",
                    "Laser surgery procedures",
                    "Optical coherence tomography",
                    "Photodynamic therapy"
                ],
                "applications": ["Surgical lasers", "Optical diagnostics", "Phototherapy", "Biomedical sensors"]
            }
        }
    },
    "computational_physics": {
        "title": "Computational Physics",
        "icon": "fas fa-laptop-code",
        "color": "info",
        "description": "Numerical methods and computer simulations in physics",
        "subtopics": {
            "numerical_methods": {
                "title": "Numerical Methods",
                "description": "Mathematical techniques for physics problems",
                "formulas": {
                    "x_{n+1} = x_n - f(x_n)/f'(x_n)": "Newton-Raphson method",
                    "y_{n+1} = y_n + h × f(x_n, y_n)": "Euler's method",
                    "∫f(x)dx ≈ h/3[f(x₀) + 4f(x₁) + f(x₂)]": "Simpson's rule",
                    "∂u/∂t = D∇²u": "Diffusion equation",
                    "E = ∑ᵢ ½mᵢvᵢ² + ∑ᵢ<ⱼ U(rᵢⱼ)": "Molecular dynamics energy"
                },
                "examples": [
                    "Weather prediction models",
                    "Quantum mechanics calculations",
                    "Fluid dynamics simulations",
                    "Particle physics Monte Carlo"
                ],
                "applications": ["Scientific computing", "Engineering simulation", "Data analysis", "Machine learning"]
            },
            "monte_carlo_methods": {
                "title": "Monte Carlo Methods",
                "description": "Statistical simulation techniques",
                "formulas": {
                    "⟨f⟩ = ∫f(x)P(x)dx": "Expectation value",
                    "σ² = ⟨f²⟩ - ⟨f⟩²": "Variance",
                    "σ_mean = σ/√N": "Standard error of mean",
                    "P(x) = e^(-βH(x))/Z": "Boltzmann distribution",
                    "A = ∫₀¹ f(x)dx ≈ (1/N)∑f(xᵢ)": "Monte Carlo integration"
                },
                "examples": [
                    "Random walk simulations",
                    "Statistical mechanics calculations",
                    "Financial risk modeling",
                    "Radiation transport"
                ],
                "applications": ["Risk analysis", "Optimization problems", "Statistical physics", "Quality control"]
            },
            "machine_learning_physics": {
                "title": "Machine Learning in Physics",
                "description": "AI and ML applications in physics research",
                "formulas": {
                    "J = ½∑(y - ŷ)²": "Mean squared error",
                    "∂J/∂w = X^T(Xw - y)": "Gradient for linear regression",
                    "σ(z) = 1/(1 + e^(-z))": "Sigmoid activation function",
                    "H = -∑p(x)log(p(x))": "Information entropy",
                    "KL(P||Q) = ∑P(x)log(P(x)/Q(x))": "Kullback-Leibler divergence"
                },
                "examples": [
                    "Particle physics data analysis",
                    "Astronomical object classification",
                    "Materials property prediction",
                    "Quantum state optimization"
                ],
                "applications": ["Data analysis", "Pattern recognition", "Predictive modeling", "Automated discovery"]
            }
        }
    },
    "particle_physics": {
        "title": "Particle Physics",
        "icon": "fas fa-atom",
        "color": "primary",
        "description": "Study of fundamental particles and their interactions",
        "subtopics": {
            "standard_model": {
                "title": "Standard Model",
                "description": "Fundamental particles and forces",
                "formulas": {
                    "E² = (pc)² + (mc²)²": "Relativistic energy-momentum relation",
                    "λ = h/p": "de Broglie wavelength",
                    "α = e²/(4πε₀ℏc) ≈ 1/137": "Fine structure constant",
                    "g_μν = diag(-1,1,1,1)": "Minkowski metric",
                    "L = ψ̄(iγ^μD_μ - m)ψ": "Dirac Lagrangian"
                },
                "examples": [
                    "Higgs boson discovery at LHC",
                    "Electron-positron annihilation",
                    "Quark confinement in protons",
                    "Neutrino oscillations"
                ],
                "applications": ["Particle accelerators", "Medical imaging", "Nuclear energy", "Fundamental research"]
            },
            "quantum_field_theory": {
                "title": "Quantum Field Theory",
                "description": "Quantum mechanics of fields and particles",
                "formulas": {
                    "[φ(x), π(y)] = iℏδ³(x-y)": "Canonical commutation relations",
                    "⟨0|T{φ(x)φ(y)}|0⟩": "Time-ordered correlation function",
                    "S = ∫d⁴x L(φ, ∂φ)": "Action functional",
                    "Z[J] = ∫Dφ e^(i∫(L + Jφ)d⁴x)": "Generating functional",
                    "Γ = -iℏ ln Z[J]": "Effective action"
                },
                "examples": [
                    "Virtual particle interactions",
                    "Vacuum fluctuations",
                    "Feynman diagram calculations",
                    "Spontaneous symmetry breaking"
                ],
                "applications": ["Particle physics theory", "Condensed matter physics", "Cosmology", "Quantum computing"]
            },
            "accelerator_physics": {
                "title": "Accelerator Physics",
                "description": "Physics of particle acceleration and beam dynamics",
                "formulas": {
                    "qE = dp/dt": "Lorentz force equation",
                    "ρ = p/(qB)": "Radius of curvature in magnetic field",
                    "f_s = qB/(2πγm)": "Synchrotron frequency",
                    "P_s = (2e²c)/(3(4πε₀)) × (β⁴γ⁴)/(ρ²)": "Synchrotron radiation power",
                    "ε_n = βγε": "Normalized emittance"
                },
                "examples": [
                    "Large Hadron Collider operation",
                    "Medical linear accelerators",
                    "Synchrotron light sources",
                    "Ion beam therapy"
                ],
                "applications": ["High energy physics", "Medical therapy", "Materials research", "Industrial processing"]
            }
        }
    },
    "condensed_matter": {
        "title": "Condensed Matter Physics",
        "icon": "fas fa-gem",
        "color": "secondary",
        "description": "Physics of solids, liquids, and complex materials",
        "subtopics": {
            "crystal_structure": {
                "title": "Crystal Structure and Lattices",
                "description": "Atomic arrangement in crystalline materials",
                "formulas": {
                    "nλ = 2d sin θ": "Bragg's law for X-ray diffraction",
                    "a⃗ · b⃗* = 2πδ_ab": "Reciprocal lattice relation",
                    "ρ(r⃗) = ∑_n f_n δ(r⃗ - r⃗_n)": "Electron density",
                    "F_hkl = ∑_j f_j e^(2πi(hx_j + ky_j + lz_j))": "Structure factor",
                    "E = ℏ²k²/(2m*)": "Free electron energy"
                },
                "examples": [
                    "Diamond crystal structure",
                    "Silicon semiconductor lattice",
                    "Salt crystal formation",
                    "Quasicrystal patterns"
                ],
                "applications": ["Semiconductor devices", "Materials characterization", "Drug crystallization", "Nanotechnology"]
            },
            "electronic_properties": {
                "title": "Electronic Properties",
                "description": "Electron behavior in solids",
                "formulas": {
                    "σ = nqμ": "Electrical conductivity",
                    "μ = qτ/m*": "Electron mobility",
                    "n = N_c e^(-(E_c-E_F)/kT)": "Electron concentration",
                    "R_H = 1/(nq)": "Hall coefficient",
                    "κ = (π²k²T)/(3e²ρ) × L": "Wiedemann-Franz law"
                },
                "examples": [
                    "Silicon solar cell operation",
                    "LED light emission",
                    "Superconductor zero resistance",
                    "Thermoelectric cooling"
                ],
                "applications": ["Electronics", "Solar cells", "Superconducting magnets", "Thermoelectric devices"]
            },
            "magnetism": {
                "title": "Magnetism in Materials",
                "description": "Magnetic properties and phenomena",
                "formulas": {
                    "M⃗ = χH⃗": "Magnetic susceptibility",
                    "B⃗ = μ₀(H⃗ + M⃗)": "Magnetic induction",
                    "E = -J∑S⃗ᵢ · S⃗ⱼ": "Heisenberg model",
                    "T_c = 2JS(S+1)z/(3k)": "Curie temperature (mean field)",
                    "χ = C/(T-θ)": "Curie-Weiss law"
                },
                "examples": [
                    "Ferromagnetic iron domains",
                    "Antiferromagnetic ordering",
                    "Magnetic storage devices",
                    "MRI contrast agents"
                ],
                "applications": ["Data storage", "Electric motors", "Medical imaging", "Magnetic sensors"]
            }
        }
    },
    "quantum_information": {
        "title": "Quantum Information",
        "icon": "fas fa-microchip",
        "color": "info",
        "description": "Quantum mechanics applied to information processing",
        "subtopics": {
            "quantum_computing": {
                "title": "Quantum Computing",
                "description": "Computation using quantum mechanical phenomena",
                "formulas": {
                    "|ψ⟩ = α|0⟩ + β|1⟩": "Qubit superposition",
                    "U|ψ⟩ = |ψ'⟩": "Unitary quantum gate operation",
                    "ρ = ∑ᵢ pᵢ|ψᵢ⟩⟨ψᵢ|": "Density matrix",
                    "S = -Tr(ρ log ρ)": "Von Neumann entropy",
                    "F = ⟨ψ|ρ|ψ⟩": "Fidelity measure"
                },
                "examples": [
                    "Shor's factoring algorithm",
                    "Quantum error correction",
                    "Quantum teleportation",
                    "Grover's search algorithm"
                ],
                "applications": ["Cryptography", "Optimization", "Drug discovery", "Financial modeling"]
            },
            "quantum_cryptography": {
                "title": "Quantum Cryptography",
                "description": "Secure communication using quantum mechanics",
                "formulas": {
                    "QBER = (E + e/2)/(1 + e)": "Quantum bit error rate",
                    "I(A:B) = H(A) + H(B) - H(AB)": "Mutual information",
                    "r = 1 - h(e) - f(e)": "Secret key rate",
                    "χ(E) = max_ρ S(∑ᵢ pᵢρᵢ) - ∑ᵢ pᵢS(ρᵢ)": "Holevo bound",
                    "P_error ≤ ½e^(-nE₀)": "Quantum error probability"
                },
                "examples": [
                    "BB84 quantum key distribution",
                    "Quantum random number generation",
                    "Quantum digital signatures",
                    "Device-independent protocols"
                ],
                "applications": ["Secure communications", "Banking security", "Government communications", "Internet security"]
            },
            "quantum_entanglement": {
                "title": "Quantum Entanglement",
                "description": "Non-local correlations in quantum systems",
                "formulas": {
                    "|Ψ⟩ = (|00⟩ + |11⟩)/√2": "Bell state",
                    "E(a⃗,b⃗) = ⟨Ψ|A⃗·a⃗ ⊗ B⃗·b⃗|Ψ⟩": "Correlation function",
                    "S = 2√2": "Tsirelson bound",
                    "E_N = log₂ d - S(ρ_A)": "Entanglement of formation",
                    "I₃₂₂₂ ≤ 1": "CHSH inequality"
                },
                "examples": [
                    "EPR paradox demonstration",
                    "Bell test experiments",
                    "Quantum teleportation protocols",
                    "Entanglement swapping"
                ],
                "applications": ["Quantum networks", "Quantum sensing", "Fundamental physics tests", "Quantum metrology"]
            }
        }
    },
    "nonlinear_dynamics": {
        "title": "Nonlinear Dynamics and Chaos",
        "icon": "fas fa-project-diagram",
        "color": "warning",
        "description": "Complex behavior in nonlinear systems",
        "subtopics": {
            "chaos_theory": {
                "title": "Chaos Theory",
                "description": "Deterministic systems with unpredictable behavior",
                "formulas": {
                    "x_{n+1} = rx_n(1-x_n)": "Logistic map",
                    "λ = lim_{n→∞} (1/n)∑ln|f'(x_i)|": "Lyapunov exponent",
                    "D = lim_{ε→0} ln(N(ε))/ln(1/ε)": "Fractal dimension",
                    "δ(t) = δ₀e^(λt)": "Exponential divergence",
                    "C(τ) = ⟨x(t)x(t+τ)⟩": "Correlation function"
                },
                "examples": [
                    "Weather system unpredictability",
                    "Population dynamics",
                    "Double pendulum motion",
                    "Cardiac arrhythmias"
                ],
                "applications": ["Weather prediction", "Ecosystem modeling", "Financial markets", "Engineering control"]
            },
            "fractals": {
                "title": "Fractals and Self-Similarity",
                "description": "Geometric structures with self-similar patterns",
                "formulas": {
                    "N(ε) ∝ ε^(-D)": "Box-counting dimension",
                    "z_{n+1} = z_n² + c": "Mandelbrot set iteration",
                    "L(ε) ∝ ε^(1-D)": "Fractal length scaling",
                    "M(r) ∝ r^D": "Mass scaling in fractals",
                    "f(αx) = α^H f(x)": "Self-affine scaling"
                },
                "examples": [
                    "Coastline measurement paradox",
                    "Mandelbrot set visualization",
                    "Lung bronchial structure",
                    "Stock market fluctuations"
                ],
                "applications": ["Computer graphics", "Antenna design", "Image compression", "Natural pattern analysis"]
            },
            "solitons": {
                "title": "Solitons and Integrable Systems",
                "description": "Stable wave packets in nonlinear media",
                "formulas": {
                    "∂u/∂t + u∂u/∂x + ∂³u/∂x³ = 0": "Korteweg-de Vries equation",
                    "u(x,t) = 2κ²sech²(κ(x-vt))": "KdV soliton solution",
                    "i∂ψ/∂t + ∂²ψ/∂x² + |ψ|²ψ = 0": "Nonlinear Schrödinger equation",
                    "∂²φ/∂t² - ∂²φ/∂x² + sin φ = 0": "Sine-Gordon equation",
                    "L_n = [L, A_n]": "Lax pair formulation"
                },
                "examples": [
                    "Tsunami wave propagation",
                    "Optical fiber pulse transmission",
                    "Josephson junction dynamics",
                    "DNA breathing modes"
                ],
                "applications": ["Optical communications", "Plasma physics", "Condensed matter", "Biological systems"]
            }
        }
    },
    "nanophysics": {
        "title": "Nanophysics & Nanomechanics",
        "icon": "fas fa-microscope",
        "color": "info",
        "description": "Physics at the nanoscale - where quantum effects dominate",
        "subtopics": {
            "nanoscale_mechanics": {
                "title": "Nanoscale Mechanics",
                "description": "Mechanical properties and behavior at nanometer scale",
                "formulas": {
                    "F = kx": "Hooke's law for nanosprings and cantilevers",
                    "σ = E·ε": "Stress-strain relationship for nanomaterials",
                    "k = 3EI/L³": "Spring constant of nanocantilever",
                    "f₀ = (1/2π)√(k/m*)": "Resonant frequency of nanoresonator",
                    "Q = ω₀/(2δ)": "Quality factor of nanomechanical systems"
                },
                "examples": [
                    "Carbon nanotube mechanical properties",
                    "AFM cantilever dynamics",
                    "NEMS (Nanoelectromechanical Systems)",
                    "Graphene membrane resonators"
                ],
                "applications": ["NEMS sensors", "Atomic force microscopy", "Nanoscale actuators", "Quantum sensing"]
            },
            "quantum_confinement": {
                "title": "Quantum Confinement Effects",
                "description": "Quantum mechanical effects in nanoscale structures",
                "formulas": {
                    "E_n = (n²π²ℏ²)/(2mL²)": "Particle in a box energy levels",
                    "E_g(d) = E_g(bulk) + (ℏ²π²)/(2μd²)": "Size-dependent bandgap",
                    "λ_dB = h/p": "de Broglie wavelength",
                    "a_B = 4πε₀ℏ²/(μe²)": "Bohr radius in semiconductor",
                    "R* = μe⁴/(2(4πε₀ℏ)²)": "Effective Rydberg energy"
                },
                "examples": [
                    "Quantum dots color tuning",
                    "Silicon nanowire conductance",
                    "GaAs quantum wells",
                    "Carbon nanotube band structure"
                ],
                "applications": ["Quantum dot displays", "Single photon sources", "Quantum computing", "Solar cells"]
            },
            "surface_effects": {
                "title": "Surface and Interface Physics",
                "description": "Dominant surface effects in nanostructures",
                "formulas": {
                    "γ = (∂F/∂A)_T,V,N": "Surface energy definition",
                    "ΔP = 2γ/r": "Young-Laplace equation for nanoparticles",
                    "T_m(r) = T_m(∞)[1 - 2γV_m/(rΔH_f)]": "Size-dependent melting point",
                    "μ(r) = μ(∞) + 2γV_m/r": "Chemical potential of nanoparticle",
                    "k_ads = ν exp(-E_ads/kT)": "Adsorption rate constant"
                },
                "examples": [
                    "Gold nanoparticle melting point depression",
                    "Catalytic activity of Pt nanoparticles",
                    "Surface plasmon resonance",
                    "Wetting behavior on nanostructures"
                ],
                "applications": ["Nanocatalysis", "Drug delivery", "Surface coatings", "Sensors"]
            },
            "nanoelectronics": {
                "title": "Nanoelectronics",
                "description": "Electronic transport in nanoscale devices",
                "formulas": {
                    "G = G₀T": "Landauer conductance formula",
                    "G₀ = 2e²/h": "Conductance quantum",
                    "I = (2e/h)∫T(E)[f(E-μ₁) - f(E-μ₂)]dE": "Current through nanojunction",
                    "R_K = h/e²": "von Klitzing constant",
                    "λ_F = h/√(2πmE_F)": "Fermi wavelength"
                },
                "examples": [
                    "Single molecule transistors",
                    "Quantum point contacts",
                    "Molecular electronics",
                    "Spintronics devices"
                ],
                "applications": ["Molecular computers", "Quantum devices", "Ultra-sensitive detectors", "Memory storage"]
            },
            "nanomaterials": {
                "title": "Nanomaterials Properties",
                "description": "Unique properties of materials at nanoscale",
                "formulas": {
                    "S/V = 6/d": "Surface-to-volume ratio for spherical nanoparticles",
                    "E = E₀ + α/d": "Size-dependent Young's modulus",
                    "σ_y = σ₀ + k/√d": "Hall-Petch relationship",
                    "D = D₀exp(-Q/RT)": "Diffusion coefficient",
                    "τ = τ₀exp(ΔE/kT)": "Relaxation time"
                },
                "examples": [
                    "Superparamagnetic iron oxide nanoparticles",
                    "Carbon nanotube strength",
                    "Titanium dioxide photocatalysis",
                    "Silver nanoparticle antimicrobial properties"
                ],
                "applications": ["Nanocomposites", "Medical imaging", "Water purification", "Energy storage"]
            }
        }
    },
    "artificial_intelligence": {
        "title": "Artificial Intelligence & Physics",
        "icon": "fas fa-robot",
        "color": "success",
        "description": "AI applications in physics and physics-inspired AI",
        "subtopics": {
            "machine_learning_physics": {
                "title": "Machine Learning in Physics",
                "description": "AI methods for solving physics problems",
                "formulas": {
                    "J(θ) = (1/2m)Σ(h_θ(x^i) - y^i)²": "Cost function for regression",
                    "θ := θ - α∇J(θ)": "Gradient descent update rule",
                    "P(y|x) = σ(θᵀx)": "Logistic regression probability",
                    "H(X) = -Σp(x)log₂p(x)": "Information entropy",
                    "I(X;Y) = H(X) - H(X|Y)": "Mutual information"
                },
                "examples": [
                    "Particle physics event classification",
                    "Protein folding prediction",
                    "Climate modeling with neural networks",
                    "Quantum state tomography"
                ],
                "applications": ["High energy physics", "Materials discovery", "Weather prediction", "Drug design"]
            },
            "neural_networks": {
                "title": "Neural Networks & Physics",
                "description": "Physics principles in artificial neural networks",
                "formulas": {
                    "y = σ(Wx + b)": "Neural network layer output",
                    "σ(z) = 1/(1 + e^(-z))": "Sigmoid activation function",
                    "ReLU(z) = max(0, z)": "Rectified Linear Unit",
                    "∂J/∂w = (∂J/∂a)(∂a/∂z)(∂z/∂w)": "Backpropagation chain rule",
                    "E = -Σᵢⱼwᵢⱼsᵢsⱼ": "Hopfield network energy"
                },
                "examples": [
                    "Convolutional neural networks for image recognition",
                    "Recurrent networks for time series",
                    "Transformer models for language",
                    "Physics-informed neural networks"
                ],
                "applications": ["Computer vision", "Natural language processing", "Scientific computing", "Control systems"]
            },
            "quantum_ai": {
                "title": "Quantum Artificial Intelligence",
                "description": "Quantum computing applications in AI",
                "formulas": {
                    "|ψ⟩ = α|0⟩ + β|1⟩": "Quantum superposition state",
                    "U|ψ⟩ = |ψ'⟩": "Quantum gate operation",
                    "⟨ψ|O|ψ⟩": "Quantum expectation value",
                    "ρ = Σᵢpᵢ|ψᵢ⟩⟨ψᵢ|": "Quantum density matrix",
                    "S = -Tr(ρlog₂ρ)": "Von Neumann entropy"
                },
                "examples": [
                    "Quantum machine learning algorithms",
                    "Variational quantum eigensolvers",
                    "Quantum neural networks",
                    "Quantum approximate optimization"
                ],
                "applications": ["Quantum computing", "Cryptography", "Optimization", "Simulation"]
            },
            "computational_intelligence": {
                "title": "Computational Intelligence",
                "description": "Bio-inspired and physics-based AI algorithms",
                "formulas": {
                    "x(t+1) = x(t) + v(t+1)": "Particle swarm optimization",
                    "p_select = f(x)/Σf(x)": "Selection probability in genetic algorithms",
                    "ΔE = E_new - E_old": "Energy difference in simulated annealing",
                    "P(accept) = exp(-ΔE/T)": "Metropolis acceptance probability",
                    "τ_ij(t+1) = (1-ρ)τ_ij(t) + Δτ_ij": "Pheromone update in ant colony"
                },
                "examples": [
                    "Genetic algorithms for optimization",
                    "Simulated annealing for global optimization",
                    "Ant colony optimization",
                    "Artificial immune systems"
                ],
                "applications": ["Engineering design", "Scheduling problems", "Pattern recognition", "Robotics"]
            },
            "physics_ai_applications": {
                "title": "AI Applications in Physics Research",
                "description": "How AI is revolutionizing physics research",
                "formulas": {
                    "χ² = Σ((O_i - E_i)²/E_i)": "Chi-square goodness of fit",
                    "R² = 1 - SS_res/SS_tot": "Coefficient of determination",
                    "F₁ = 2(precision × recall)/(precision + recall)": "F1 score for classification",
                    "AUC = ∫₀¹TPR(FPR⁻¹(x))dx": "Area under ROC curve",
                    "RMSE = √(Σ(y_pred - y_true)²/n)": "Root mean square error"
                },
                "examples": [
                    "LIGO gravitational wave detection",
                    "LHC particle discovery",
                    "Exoplanet detection with Kepler data",
                    "Materials property prediction"
                ],
                "applications": ["Experimental physics", "Theoretical modeling", "Data analysis", "Scientific discovery"]
            }
        }
    }
}

# Simplified lists for backward compatibility
physics_topics = list(physics_topics_database.keys())
physics_lessons = {
    topic: list(data["subtopics"].keys()) 
    for topic, data in physics_topics_database.items()
}

@app.route('/')
def dashboard():
    """Physics Learning Dashboard"""
    stats = {
        'total_topics': len(physics_topics),
        'total_lessons': sum(len(lessons) for lessons in physics_lessons.values()),
        'categories': len(physics_lessons),
        'active_students': 150  # Sample data
    }
    
    return render_template('physics_dashboard_new.html', 
                         stats=stats,
                         topics=physics_topics,
                         lessons=physics_lessons)

@app.route('/lessons')
def lessons():
    """Physics Lessons Overview"""
    return render_template('physics_lessons.html', lessons=physics_lessons)

@app.route('/lesson/<category>/<lesson>')
def start_lesson(category, lesson):
    """Start a specific physics lesson"""
    # Get lesson data from the comprehensive database
    if category in physics_topics_database and lesson in physics_topics_database[category]['subtopics']:
        lesson_data = physics_topics_database[category]['subtopics'][lesson]
        category_data = physics_topics_database[category]
        
        # Create comprehensive lesson content
        lesson_content = {
            'category': category_data['title'],
            'lesson_title': lesson_data['title'],
            'description': lesson_data['description'],
            'formulas': lesson_data['formulas'],
            'examples': lesson_data['examples'],
            'applications': lesson_data['applications'],
            'icon': category_data['icon'],
            'color': category_data['color']
        }
        
        return render_template('lesson_detail.html', lesson=lesson_content)
    else:
        # Fallback for lessons not in database
        return render_template('lesson_detail.html', lesson={
            'category': category.title(),
            'lesson_title': lesson.replace('_', ' ').title(),
            'description': f"Comprehensive lesson on {lesson.replace('_', ' ')}",
            'formulas': {"Coming Soon": "Detailed formulas will be added"},
            'examples': ["Interactive examples coming soon"],
            'applications': ["Real-world applications"],
            'icon': 'fas fa-atom',
            'color': 'primary'
        })

@app.route('/topics')
def topics():
    """Physics Topics Overview"""
    return render_template('physics_topics.html', topics=physics_topics)

@app.route('/practice')
def practice():
    """JAMB Practice Questions"""
    return render_template('physics_practice.html')

@app.route('/progress')
def progress():
    """Student Progress Tracking"""
    progress_data = {
        'completed_topics': 3,
        'total_topics': len(physics_topics),
        'quiz_scores': [85, 92, 78, 88],
        'current_level': 'Intermediate'
    }
    return render_template('physics_progress.html', progress=progress_data)

@app.route('/classroom')
def classroom():
    """Show animated classroom with teacher and students"""
    return render_template('classroom.html')

@app.route('/api/speak', methods=['POST'])
def speak_text():
    """Text-to-speech API endpoint"""
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'en')
    
    if not text:
        return jsonify({'error': 'No text provided'})
    
    try:
        # Return success - actual speech will be handled by browser
        return jsonify({
            'success': True, 
            'text': text, 
            'language': language,
            'message': 'Speech request processed'
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/ai-tutor', methods=['POST'])
def ai_tutor():
    """Universal AI Tutor - Answers ANY question asked"""
    data = request.get_json()
    question = data.get('question', '').lower()
    level = data.get('level', 'auto')  # auto, basic, intermediate, advanced, olympiad
    exam_focus = data.get('exam_focus', 'jamb')  # jamb, waec, neco, olympiad
    
    # Universal Knowledge Base - Can answer ANY question
    def get_universal_response(question, detected_level='intermediate'):
        """Generate intelligent responses for ANY question"""
        
        # Physics questions - use existing comprehensive database
        for topic_key, topic_data in physics_topics_database.items():
            for subtopic_key, subtopic_data in topic_data['subtopics'].items():
                if any(keyword in question for keyword in [subtopic_key, topic_key, subtopic_data['title'].lower()]):
                    formulas = list(subtopic_data['formulas'].keys())[:3]
                    examples = subtopic_data['examples'][:2]
                    
                    if detected_level == 'basic':
                        return f"Let me explain {subtopic_data['title']} simply! {subtopic_data['description']} Key formulas: {', '.join(formulas)}. Examples: {', '.join(examples)}. Think of it like everyday situations you see around you!"
                    elif detected_level == 'intermediate':
                        return f"{subtopic_data['title']}: {subtopic_data['description']} Important formulas: {', '.join(formulas)}. Real examples: {', '.join(examples)}. Applications: {', '.join(subtopic_data['applications'][:2])}"
                    elif detected_level == 'advanced':
                        return f"Advanced {subtopic_data['title']}: {subtopic_data['description']} Mathematical formulations: {', '.join(formulas)}. Complex applications: {', '.join(subtopic_data['applications'])}."
                    elif detected_level == 'olympiad':
                        return f"Olympiad-level {subtopic_data['title']}: {subtopic_data['description']} Master these formulas: {', '.join(formulas)}. Advanced applications: {', '.join(subtopic_data['applications'])}."
        
        # Mathematics questions
        math_responses = {
            'algebra': "Algebra is about finding unknown values using equations. Key concepts: variables (x, y), equations (2x + 3 = 7), and solving for unknowns. Practice with linear equations, quadratic formulas, and factoring.",
            'calculus': "Calculus studies rates of change (derivatives) and areas under curves (integrals). Derivatives: d/dx(x²) = 2x. Integrals: ∫x²dx = x³/3 + C. Essential for physics and engineering!",
            'geometry': "Geometry deals with shapes, angles, and spatial relationships. Key formulas: Area of circle = πr², Pythagorean theorem: a² + b² = c², Volume of sphere = (4/3)πr³.",
            'trigonometry': "Trigonometry relates angles to side lengths in triangles. Key functions: sin, cos, tan. Remember: SOH-CAH-TOA. sin(θ) = opposite/hypotenuse, cos(θ) = adjacent/hypotenuse, tan(θ) = opposite/adjacent.",
            'statistics': "Statistics analyzes data and probability. Key concepts: mean (average), median (middle value), mode (most frequent), standard deviation (spread), and probability (chance of events)."
        }
        
        # Chemistry questions
        chemistry_responses = {
            'atoms': "Atoms are the basic building blocks of matter. They contain protons (+), neutrons (neutral), and electrons (-). Atomic number = number of protons. Mass number = protons + neutrons.",
            'molecules': "Molecules are groups of atoms bonded together. Water (H₂O) has 2 hydrogen atoms and 1 oxygen atom. Chemical bonds include ionic (electron transfer) and covalent (electron sharing).",
            'reactions': "Chemical reactions rearrange atoms to form new substances. Balance equations: reactants → products. Conservation of mass: atoms are neither created nor destroyed, only rearranged.",
            'periodic table': "The periodic table organizes elements by atomic number. Groups (columns) have similar properties. Periods (rows) show electron shell patterns. Metals on left, nonmetals on right.",
            'acids': "Acids release H⁺ ions in water (pH < 7). Bases release OH⁻ ions (pH > 7). Strong acids: HCl, H₂SO₄. Strong bases: NaOH, KOH. Neutralization: acid + base → salt + water."
        }
        
        # Biology questions
        biology_responses = {
            'cells': "Cells are the basic units of life. Prokaryotes (bacteria) lack nucleus. Eukaryotes (plants, animals) have nucleus. Key organelles: mitochondria (energy), chloroplasts (photosynthesis), ribosomes (protein synthesis).",
            'dna': "DNA (deoxyribonucleic acid) stores genetic information. Double helix structure with base pairs: A-T and G-C. DNA → RNA → Protein (central dogma). Genes are DNA segments coding for traits.",
            'evolution': "Evolution explains how species change over time. Natural selection: favorable traits increase survival and reproduction. Evidence: fossils, DNA similarities, embryology, biogeography.",
            'photosynthesis': "Plants convert sunlight into chemical energy. Equation: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂. Occurs in chloroplasts using chlorophyll. Produces glucose and oxygen.",
            'genetics': "Genetics studies heredity and variation. Mendel's laws: dominance, segregation, independent assortment. Genotype (genetic makeup) vs phenotype (observable traits). Punnett squares predict offspring."
        }
        
        # General knowledge and other subjects
        general_responses = {
            'history': "I can help with historical events, dates, and their significance. What specific historical period or event interests you?",
            'geography': "Geography studies Earth's features, climates, and human activities. I can explain physical geography (landforms, weather) or human geography (populations, cultures).",
            'literature': "Literature includes novels, poetry, drama, and essays. I can discuss themes, literary devices, famous authors, and analysis techniques.",
            'computer science': "Computer science covers programming, algorithms, data structures, and software development. What programming concept would you like to explore?",
            'economics': "Economics studies how societies allocate scarce resources. Key concepts: supply and demand, inflation, GDP, market structures, and economic policies.",
            'psychology': "Psychology studies human behavior and mental processes. Areas include cognitive, social, developmental, and clinical psychology.",
            'philosophy': "Philosophy explores fundamental questions about existence, knowledge, values, and reasoning. Major branches: metaphysics, epistemology, ethics, logic.",
            'art': "Art encompasses visual arts, music, theater, and creative expression. I can discuss techniques, history, famous artists, and artistic movements.",
            'music': "Music theory covers rhythm, melody, harmony, and composition. I can explain scales, chords, musical forms, and famous composers.",
            'sports': "Sports involve physical activity and competition. I can discuss rules, techniques, famous athletes, and the science behind athletic performance."
        }
        
        # Check for specific subject keywords
        for subject, response in {**math_responses, **chemistry_responses, **biology_responses, **general_responses}.items():
            if subject in question or any(keyword in question for keyword in subject.split()):
                return f"📚 {response}"
        
        # Personal questions and greetings
        if any(greeting in question for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            return "Hello! I'm Engineer Clement Ekelemchi, your AI tutor. I can answer ANY question you have - physics, mathematics, chemistry, biology, history, literature, or anything else you're curious about! What would you like to learn today?"
        
        if any(personal in question for personal in ['who are you', 'what are you', 'your name']):
            return "I'm Engineer Clement Ekelemchi, your comprehensive AI tutor! I'm here to help you learn anything - from physics and mathematics to history, literature, science, and beyond. I can explain concepts at any level from basic to advanced. What subject interests you?"
        
        if any(help_word in question for help in ['help', 'assist', 'support']):
            return "I'm here to help! I can answer questions on virtually any topic: 📚 Sciences (Physics, Chemistry, Biology), 🔢 Mathematics, 📖 Literature & History, 💻 Technology, 🎨 Arts, and much more! Just ask me anything you're curious about."
        
        # Current events and factual questions
        if any(current in question for current in ['news', 'current', 'today', 'recent', 'latest']):
            return "I can help explain concepts and provide educational information, but I don't have access to real-time news. However, I can explain the science, history, or context behind current topics you're interested in!"
        
        # How-to questions
        if question.startswith('how to') or 'how do i' in question or 'how can i' in question:
            return f"Great question! I'd love to help you learn how to do that. Could you be more specific about what you'd like to learn? I can provide step-by-step explanations for academic topics, problem-solving techniques, or study methods."
        
        # Why questions
        if question.startswith('why') or 'why does' in question or 'why is' in question:
            return f"Excellent question! Understanding 'why' is key to deep learning. I can explain the reasoning, causes, or principles behind almost any phenomenon. What specifically would you like to understand?"
        
        # What questions
        if question.startswith('what') or 'what is' in question or 'what are' in question:
            return f"I can explain what that is! I have knowledge across many subjects. Could you be more specific about the topic you're asking about? I can provide definitions, explanations, and examples."
        
        # Default comprehensive response for any question
        return f"That's an interesting question! I'm Engineer Clement Ekelemchi, and I can help you understand virtually any topic. While I specialize in physics and sciences, I can also explain mathematics, chemistry, biology, history, literature, arts, and much more. Could you provide a bit more detail about what specifically you'd like to know? I'll give you a clear, helpful explanation at the right level for you!"
    
    # Detect student level from question complexity
    def detect_level(question):
        basic_indicators = ['simple', 'easy', 'basic', 'like i\'m 10', 'explain simply', 'what is', 'eli5']
        advanced_indicators = ['derive', 'proof', 'complex', 'detailed', 'advanced', 'technical', 'research']
        olympiad_indicators = ['olympiad', 'competition', 'expert level', 'professional']
        
        if any(indicator in question for indicator in olympiad_indicators):
            return 'olympiad'
        elif any(indicator in question for indicator in advanced_indicators):
            return 'advanced'
        elif any(indicator in question for indicator in basic_indicators):
            return 'basic'
        else:
            return 'intermediate'
    
    # Detect level if not specified
    if level == 'auto':
        level = detect_level(question)
    
    # Generate universal response
    response = get_universal_response(question, level)
    
    # Add level-appropriate follow-up
    if level == 'basic':
        response += "\n\n🤔 Would you like me to explain this differently or give you more examples?"
    elif level == 'intermediate':
        response += "\n\n📝 Need more details or have a follow-up question?"
    elif level in ['advanced', 'olympiad']:
        response += "\n\n🧠 Would you like me to go deeper into this topic or explore related concepts?"
    
    # Add encouraging note
    response += "\n\n💡 Remember: No question is too simple or too complex. I'm here to help you learn anything!"
    
    return jsonify({
        'response': response,
        'level': level,
        'exam_focus': exam_focus,
        'tutor': 'Engineer Clement Ekelemchi',
        'timestamp': datetime.now().isoformat(),
        'adaptive_note': f"Universal response tailored for {level} level",
        'capabilities': "I can answer questions on ANY topic - just ask!"
    })

@app.route('/tutor')
def ai_tutor_page():
    """AI Physics Tutor Chat Interface"""
    return render_template('ai_tutor.html')

@app.route('/virtual-lab')
def virtual_lab():
    """AI-Guided Virtual Physics Laboratory"""
    return render_template('virtual_lab.html')

@app.route('/api/track-understanding', methods=['POST'])
def track_understanding():
    """Track student understanding and trigger re-teaching if needed"""
    data = request.get_json()
    topic = data.get('topic', '')
    understanding_score = data.get('score', 0)  # 0-100
    question_type = data.get('type', 'concept')  # concept, calculation, application
    
    # Simple understanding tracking (in production, use a database)
    session_data = {
        'topic': topic,
        'score': understanding_score,
        'needs_reteaching': understanding_score < 70,
        'suggested_level': 'basic' if understanding_score < 50 else 'intermediate' if understanding_score < 80 else 'advanced'
    }
    
    response = {
        'needs_reteaching': session_data['needs_reteaching'],
        'suggested_level': session_data['suggested_level'],
        'encouragement': get_encouragement_message(understanding_score),
        'next_steps': get_next_steps(topic, understanding_score)
    }
    
    return jsonify(response)

def get_encouragement_message(score):
    """Generate encouraging messages based on performance"""
    if score >= 90:
        return "Excellent! You've mastered this concept! 🌟 Ready for more advanced challenges?"
    elif score >= 70:
        return "Great job! You're getting it! 👍 Let's practice a bit more to solidify your understanding."
    elif score >= 50:
        return "Good effort! 💪 You're on the right track. Let me explain this differently to help you understand better."
    else:
        return "No worries! 😊 Physics can be tricky. Let's break this down into smaller, simpler steps."

def get_next_steps(topic, score):
    """Suggest next learning steps based on performance"""
    if score >= 80:
        return f"Try advanced {topic} problems or move to the next topic."
    elif score >= 60:
        return f"Practice more {topic} calculations and real-world applications."
    else:
        return f"Let's review {topic} basics with simpler explanations and examples."

# Global student behavior tracking (in production, use a database)
student_patterns = {
    'answer_history': [],
    'mistake_patterns': {},
    'learning_style': 'visual',
    'common_errors': [],
    'response_times': [],
    'confidence_levels': []
}

@app.route('/api/predict-mistakes', methods=['POST'])
def predict_mistakes():
    """Advanced mistake prediction system"""
    data = request.get_json()
    question_type = data.get('question_type', '')
    student_answer = data.get('answer', '')
    correct_answer = data.get('correct_answer', '')
    response_time = data.get('response_time', 0)
    confidence = data.get('confidence', 50)
    
    # Analyze student's answer pattern
    mistake_analysis = analyze_answer_pattern(student_answer, correct_answer, question_type)
    
    # Predict next likely mistakes
    predicted_mistakes = predict_next_mistakes(question_type, mistake_analysis)
    
    # Generate preventive intervention
    intervention = generate_preventive_intervention(predicted_mistakes, question_type)
    
    # Update student pattern tracking
    update_student_patterns(student_answer, correct_answer, response_time, confidence, mistake_analysis)
    
    return jsonify({
        'predicted_mistakes': predicted_mistakes,
        'intervention': intervention,
        'confidence_score': calculate_prediction_confidence(mistake_analysis),
        'learning_recommendations': get_personalized_recommendations(mistake_analysis)
    })

def analyze_answer_pattern(student_answer, correct_answer, question_type):
    """Analyze student's answer to identify mistake patterns"""
    analysis = {
        'mistake_type': 'none',
        'error_category': '',
        'conceptual_gap': '',
        'calculation_error': False,
        'unit_error': False,
        'formula_confusion': False,
        'sign_error': False,
        'magnitude_error': False
    }
    
    if not student_answer or student_answer.lower() == correct_answer.lower():
        return analysis
    
    # Common physics mistake patterns
    mistake_patterns = {
        'force_problems': {
            'forgot_direction': ['negative', 'opposite', 'direction'],
            'wrong_formula': ['ma', 'f=ma', 'acceleration'],
            'unit_confusion': ['kg', 'newton', 'n', 'm/s'],
            'free_body_diagram': ['forces', 'diagram', 'components']
        },
        'energy_problems': {
            'kinetic_potential_confusion': ['ke', 'pe', 'kinetic', 'potential'],
            'conservation_violation': ['energy', 'conservation', 'total'],
            'work_energy_mix': ['work', 'energy', 'joule'],
            'height_reference': ['height', 'reference', 'ground']
        },
        'wave_problems': {
            'frequency_period_confusion': ['frequency', 'period', 'hz', 'hertz'],
            'wave_speed_formula': ['v=fl', 'velocity', 'wavelength'],
            'amplitude_confusion': ['amplitude', 'intensity', 'loudness'],
            'wave_type_confusion': ['longitudinal', 'transverse', 'sound', 'light']
        }
    }
    
    # Detect specific mistake types
    student_lower = student_answer.lower()
    
    # Check for calculation errors
    try:
        if any(char.isdigit() for char in student_answer):
            # Extract numbers and check magnitude
            import re
            student_numbers = re.findall(r'\d+\.?\d*', student_answer)
            correct_numbers = re.findall(r'\d+\.?\d*', correct_answer)
            
            if student_numbers and correct_numbers:
                student_val = float(student_numbers[0])
                correct_val = float(correct_numbers[0])
                
                if abs(student_val - correct_val) / correct_val > 0.1:
                    analysis['calculation_error'] = True
                    analysis['magnitude_error'] = abs(student_val) != abs(correct_val)
    except:
        pass
    
    # Check for unit errors
    units = ['m', 'kg', 'n', 'j', 'w', 'm/s', 'm/s²', 'hz', 'v', 'a', 'ω']
    student_units = [unit for unit in units if unit in student_lower]
    correct_units = [unit for unit in units if unit in correct_answer.lower()]
    
    if student_units != correct_units:
        analysis['unit_error'] = True
    
    # Check for sign errors
    if '-' in correct_answer and '-' not in student_answer:
        analysis['sign_error'] = True
    elif '-' in student_answer and '-' not in correct_answer:
        analysis['sign_error'] = True
    
    # Determine mistake category
    if analysis['calculation_error']:
        analysis['mistake_type'] = 'calculation'
        analysis['error_category'] = 'mathematical'
    elif analysis['unit_error']:
        analysis['mistake_type'] = 'units'
        analysis['error_category'] = 'dimensional'
    elif analysis['sign_error']:
        analysis['mistake_type'] = 'sign'
        analysis['error_category'] = 'directional'
    else:
        analysis['mistake_type'] = 'conceptual'
        analysis['error_category'] = 'understanding'
    
    return analysis

def predict_next_mistakes(question_type, current_analysis):
    """Predict what mistakes the student is likely to make next"""
    
    # Common mistake progression patterns
    mistake_progressions = {
        'calculation': [
            'Will likely make arithmetic errors in multi-step problems',
            'May forget to square velocity in kinetic energy calculations',
            'Might confuse multiplication and division in formulas'
        ],
        'units': [
            'Will probably forget to convert units in next problem',
            'May mix up SI and non-SI units',
            'Likely to drop units entirely in calculations'
        ],
        'sign': [
            'Will likely ignore direction in vector problems',
            'May forget negative signs in displacement problems',
            'Might confuse positive and negative work'
        ],
        'conceptual': [
            'Will likely apply wrong physics principle',
            'May confuse similar concepts (like KE and PE)',
            'Might use inappropriate formulas for the situation'
        ]
    }
    
    # Get student's mistake history pattern
    historical_mistakes = student_patterns.get('common_errors', [])
    
    # Predict based on current mistake and history
    predictions = []
    
    if current_analysis['mistake_type'] in mistake_progressions:
        predictions.extend(mistake_progressions[current_analysis['mistake_type']])
    
    # Add predictions based on question type
    if 'force' in question_type.lower():
        predictions.append('May forget to consider all forces acting on the object')
        predictions.append('Likely to confuse mass and weight')
    elif 'energy' in question_type.lower():
        predictions.append('Will probably mix up kinetic and potential energy')
        predictions.append('May violate conservation of energy')
    elif 'wave' in question_type.lower():
        predictions.append('Likely to confuse frequency and wavelength')
        predictions.append('May forget wave speed formula v = fλ')
    
    # Personalize based on student history
    if 'calculation' in historical_mistakes:
        predictions.append('Based on your history, watch out for arithmetic errors')
    if 'units' in historical_mistakes:
        predictions.append('Remember to check your units - you\'ve missed this before')
    
    return predictions[:3]  # Return top 3 predictions

def generate_preventive_intervention(predicted_mistakes, question_type):
    """Generate specific interventions to prevent predicted mistakes"""
    
    interventions = []
    
    for mistake in predicted_mistakes:
        if 'arithmetic' in mistake or 'calculation' in mistake:
            interventions.append({
                'type': 'calculation_check',
                'message': '🧮 Before you calculate, let me remind you: double-check your arithmetic. Would you like me to walk through the calculation step by step?',
                'action': 'Show calculation steps'
            })
        
        elif 'units' in mistake or 'convert' in mistake:
            interventions.append({
                'type': 'unit_reminder',
                'message': '📏 Unit check! Remember to convert all quantities to SI units before calculating. Need help with unit conversion?',
                'action': 'Show unit conversion'
            })
        
        elif 'direction' in mistake or 'sign' in mistake:
            interventions.append({
                'type': 'direction_warning',
                'message': '🧭 Direction matters! Remember to consider the direction of forces, velocities, and displacements. Draw a diagram if needed.',
                'action': 'Show direction guide'
            })
        
        elif 'formula' in mistake or 'principle' in mistake:
            interventions.append({
                'type': 'concept_clarification',
                'message': '💡 Concept check! Make sure you\'re using the right physics principle. Let me clarify the concept before you proceed.',
                'action': 'Explain concept'
            })
    
    # Add question-specific interventions
    if 'force' in question_type.lower():
        interventions.append({
            'type': 'force_reminder',
            'message': '⚖️ Force problems: Remember Newton\'s laws and draw free body diagrams!',
            'action': 'Show force analysis'
        })
    
    return interventions[:2]  # Return top 2 interventions

def update_student_patterns(student_answer, correct_answer, response_time, confidence, analysis):
    """Update student learning patterns for better predictions"""
    
    # Add to answer history
    student_patterns['answer_history'].append({
        'answer': student_answer,
        'correct': correct_answer,
        'time': response_time,
        'confidence': confidence,
        'analysis': analysis
    })
    
    # Update mistake patterns
    mistake_type = analysis['mistake_type']
    if mistake_type != 'none':
        if mistake_type in student_patterns['mistake_patterns']:
            student_patterns['mistake_patterns'][mistake_type] += 1
        else:
            student_patterns['mistake_patterns'][mistake_type] = 1
        
        # Add to common errors if frequent
        if student_patterns['mistake_patterns'][mistake_type] >= 2:
            if mistake_type not in student_patterns['common_errors']:
                student_patterns['common_errors'].append(mistake_type)
    
    # Track response times and confidence
    student_patterns['response_times'].append(response_time)
    student_patterns['confidence_levels'].append(confidence)
    
    # Keep only recent history (last 20 answers)
    if len(student_patterns['answer_history']) > 20:
        student_patterns['answer_history'] = student_patterns['answer_history'][-20:]

def calculate_prediction_confidence(analysis):
    """Calculate how confident we are in our mistake predictions"""
    
    base_confidence = 60
    
    # Increase confidence based on historical data
    history_length = len(student_patterns['answer_history'])
    if history_length > 5:
        base_confidence += min(20, history_length * 2)
    
    # Increase confidence if we've seen this mistake type before
    mistake_type = analysis['mistake_type']
    if mistake_type in student_patterns['mistake_patterns']:
        frequency = student_patterns['mistake_patterns'][mistake_type]
        base_confidence += min(15, frequency * 5)
    
    return min(95, base_confidence)

def get_personalized_recommendations(analysis):
    """Get personalized learning recommendations based on mistake patterns"""
    
    recommendations = []
    
    # Based on current mistake
    if analysis['mistake_type'] == 'calculation':
        recommendations.append('Practice mental math and use a calculator for complex calculations')
        recommendations.append('Break down multi-step problems into smaller parts')
    
    elif analysis['mistake_type'] == 'units':
        recommendations.append('Always write units with every number in your calculations')
        recommendations.append('Practice unit conversion problems daily')
    
    elif analysis['mistake_type'] == 'conceptual':
        recommendations.append('Review the fundamental concepts before attempting problems')
        recommendations.append('Use analogies and real-world examples to understand concepts')
    
    # Based on student patterns
    common_errors = student_patterns.get('common_errors', [])
    if 'calculation' in common_errors:
        recommendations.append('Consider using step-by-step calculation templates')
    
    if len(student_patterns.get('response_times', [])) > 0:
        avg_time = sum(student_patterns['response_times']) / len(student_patterns['response_times'])
        if avg_time < 30:  # Very fast responses
            recommendations.append('Take more time to think through problems carefully')
        elif avg_time > 180:  # Very slow responses
            recommendations.append('Practice similar problems to improve speed and confidence')
    
    return recommendations[:3]

@app.route('/api/physics-data')
def api_physics_data():
    """API endpoint for physics learning data"""
    physics_data = {
        'topics': physics_topics,
        'lessons': physics_lessons,
        'total_lessons': sum(len(lessons) for lessons in physics_lessons.values()),
        'categories': list(physics_lessons.keys())
    }
    return jsonify(physics_data)

@app.route('/api/physics-database')
def api_physics_database():
    """API endpoint for comprehensive physics database"""
    return jsonify(physics_topics_database)

@app.route('/api/physics-topic/<topic>')
def api_physics_topic(topic):
    """API endpoint for specific physics topic"""
    if topic in physics_topics_database:
        return jsonify(physics_topics_database[topic])
    else:
        return jsonify({'error': 'Topic not found'}), 404

@app.route('/encyclopedia')
def encyclopedia():
    """Comprehensive Physics Encyclopedia"""
    return render_template('physics_encyclopedia.html', topics=physics_topics_database)

@app.route('/physics-encyclopedia')
def physics_encyclopedia():
    """Comprehensive Physics Encyclopedia"""
    return render_template('physics_encyclopedia.html', 
                         physics_db=physics_topics_database)

@app.route('/api/lab-instructor', methods=['POST'])
def lab_instructor():
    """AI Lab Instructor endpoint for providing guidance and feedback"""
    data = request.get_json()
    experiment_type = data.get('experiment', 'projectile')
    action = data.get('action', 'guidance')
    experiment_data = data.get('data', {})
    
    # Generate instructor response based on experiment and data
    if experiment_type == 'projectile':
        response = generate_projectile_instructor_response(action, experiment_data)
    elif experiment_type == 'pendulum':
        response = generate_pendulum_instructor_response(action, experiment_data)
    elif experiment_type == 'springs':
        response = generate_springs_instructor_response(action, experiment_data)
    elif experiment_type == 'waves':
        response = generate_waves_instructor_response(action, experiment_data)
    else:
        response = {
            'message': 'Welcome to the virtual physics laboratory! I\'m Engineer Clement Ekelemchi, your lab instructor.',
            'guidance': 'Select an experiment to begin your investigation.',
            'next_steps': ['Choose an experiment from the list', 'Read the objectives', 'Start collecting data']
        }
    
    return jsonify(response)

def generate_projectile_instructor_response(action, data):
    """Generate instructor responses for projectile motion experiments"""
    
    if action == 'start':
        return {
            'message': 'Excellent! We\'re starting the projectile motion experiment. This is one of the most fundamental concepts in physics.',
            'guidance': 'We\'ll investigate how launch angle affects the range of a projectile. Remember, the theoretical optimal angle is 45° for maximum range in a vacuum.',
            'next_steps': [
                'Start with a 45° angle to see the baseline',
                'Try angles above and below 45°',
                'Record at least 5 different angles',
                'Observe the parabolic trajectory'
            ],
            'physics_insight': 'The range equation R = (v²sin(2θ))/g shows that range depends on sin(2θ), which is maximum when θ = 45°.'
        }
    
    elif action == 'feedback' and data:
        angle = data.get('angle', 0)
        range_val = data.get('range', 0)
        trial_count = data.get('trial_count', 0)
        
        feedback_messages = []
        
        if trial_count == 1:
            feedback_messages.append(f"Great first launch! At {angle}° you achieved {range_val:.1f}m range.")
            if angle == 45:
                feedback_messages.append("You started with the theoretical optimum angle - excellent choice!")
            elif angle < 45:
                feedback_messages.append("Try increasing the angle to see if you can get better range.")
            else:
                feedback_messages.append("Try decreasing the angle to see how it affects the range.")
        
        elif trial_count >= 2:
            if angle < 30:
                feedback_messages.append("Low angles give flatter trajectories but may not maximize range.")
            elif angle > 60:
                feedback_messages.append("High angles give more height but less horizontal distance.")
            else:
                feedback_messages.append("You're in the optimal range! Notice how small angle changes affect the range.")
        
        return {
            'message': ' '.join(feedback_messages),
            'guidance': 'Continue experimenting with different angles to map out the complete relationship.',
            'physics_insight': f'At {angle}°, sin(2θ) = {abs(math.sin(2 * math.radians(angle))):.3f}. Compare this with sin(90°) = 1.0 at the optimal 45°.'
        }
    
    elif action == 'analysis' and data:
        trials = data.get('trials', [])
        if len(trials) >= 3:
            max_range = max(trial['range'] for trial in trials)
            optimal_trial = next(trial for trial in trials if trial['range'] == max_range)
            
            return {
                'message': f'Excellent data collection! Your maximum range was {max_range:.1f}m at {optimal_trial["angle"]}°.',
                'guidance': 'Your experimental results show the classic projectile motion relationship.',
                'analysis': {
                    'optimal_angle_experimental': optimal_trial['angle'],
                    'optimal_angle_theoretical': 45,
                    'deviation': abs(optimal_trial['angle'] - 45),
                    'max_range': max_range
                },
                'physics_insight': 'The slight deviation from 45° might be due to air resistance or measurement precision in real-world conditions.'
            }
    
    return {
        'message': 'Continue your experiment and collect more data points.',
        'guidance': 'Try different angles systematically to see the complete picture.',
        'next_steps': ['Vary the angle in 15° increments', 'Record all measurements carefully', 'Look for patterns in your data']
    }

def generate_pendulum_instructor_response(action, data):
    """Generate instructor responses for pendulum experiments"""
    return {
        'message': 'The simple pendulum experiment will help you understand periodic motion.',
        'guidance': 'We\'ll investigate how pendulum length affects the period of oscillation.',
        'physics_insight': 'The period T = 2π√(L/g) shows that period depends on length, not mass or amplitude (for small angles).'
    }

def generate_springs_instructor_response(action, data):
    """Generate instructor responses for spring experiments"""
    return {
        'message': 'Hooke\'s Law experiment demonstrates the linear relationship between force and extension.',
        'guidance': 'We\'ll apply different forces and measure the resulting extensions.',
        'physics_insight': 'Hooke\'s Law states F = kx, where k is the spring constant and x is the extension.'
    }

def generate_waves_instructor_response(action, data):
    """Generate instructor responses for wave experiments"""
    return {
        'message': 'Wave properties experiment will show you the fundamental wave equation.',
        'guidance': 'We\'ll vary frequency and observe changes in wavelength.',
        'physics_insight': 'The wave equation v = fλ relates wave speed, frequency, and wavelength.'
    }

@app.route('/api/generate-lab-report', methods=['POST'])
def generate_lab_report():
    """Generate comprehensive lab reports based on experimental data"""
    data = request.get_json()
    experiment_type = data.get('experiment', 'projectile')
    lab_data = data.get('data', [])
    student_info = data.get('student_info', {})
    
    if experiment_type == 'projectile':
        report = generate_projectile_report(lab_data, student_info)
    else:
        report = {
            'title': f'{experiment_type.title()} Experiment Report',
            'content': 'Report generation for this experiment type is coming soon.',
            'status': 'pending'
        }
    
    return jsonify(report)

def generate_projectile_report(lab_data, student_info):
    """Generate detailed projectile motion lab report"""
    import math
    from datetime import datetime
    
    if not lab_data:
        return {'error': 'No experimental data provided'}
    
    # Calculate statistics
    max_range = max(trial['range'] for trial in lab_data)
    min_range = min(trial['range'] for trial in lab_data)
    avg_range = sum(trial['range'] for trial in lab_data) / len(lab_data)
    optimal_trial = next(trial for trial in lab_data if trial['range'] == max_range)
    
    # Theoretical calculations
    theoretical_max_range = (optimal_trial['velocity'] ** 2) / 9.81  # At 45°
    
    report = {
        'title': 'Projectile Motion: Angle vs Range Analysis',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'student': student_info.get('name', 'Physics Student'),
        'instructor': 'Engineer Clement Ekelemchi',
        'experiment_type': 'Projectile Motion',
        'summary': {
            'trials_conducted': len(lab_data),
            'max_range': round(max_range, 2),
            'optimal_angle_experimental': optimal_trial['angle'],
            'optimal_angle_theoretical': 45,
            'deviation_from_theory': abs(optimal_trial['angle'] - 45),
            'theoretical_max_range': round(theoretical_max_range, 2),
            'experimental_efficiency': round((max_range / theoretical_max_range) * 100, 1)
        },
        'sections': {
            'objective': 'To investigate the relationship between launch angle and horizontal range in projectile motion, and to determine the optimal angle for maximum range.',
            'theory': {
                'range_equation': 'R = (v₀²sin(2θ))/g',
                'optimal_angle': '45° (when sin(2θ) = 1)',
                'key_variables': ['Initial velocity (v₀)', 'Launch angle (θ)', 'Gravitational acceleration (g = 9.81 m/s²)']
            },
            'methodology': [
                'Set up virtual projectile launcher',
                'Vary launch angle while keeping initial velocity constant',
                'Measure horizontal range for each angle',
                'Record trajectory data and flight time',
                'Analyze relationship between angle and range'
            ],
            'results': lab_data,
            'analysis': {
                'range_variation': f'Range varied from {min_range:.1f}m to {max_range:.1f}m',
                'optimal_performance': f'Maximum range of {max_range:.1f}m achieved at {optimal_trial["angle"]}°',
                'theory_comparison': f'Experimental optimum deviates {abs(optimal_trial["angle"] - 45):.1f}° from theoretical 45°',
                'efficiency': f'Achieved {round((max_range / theoretical_max_range) * 100, 1)}% of theoretical maximum range'
            },
            'conclusions': [
                'Projectile range varies with launch angle as predicted by theory',
                f'Experimental optimal angle ({optimal_trial["angle"]}°) closely matches theoretical prediction (45°)',
                'Range decreases for angles both above and below the optimum',
                'Results confirm the sin(2θ) dependence in the range equation'
            ],
            'applications': [
                'Sports ballistics (basketball, football, javelin)',
                'Military artillery calculations',
                'Space mission trajectory planning',
                'Engineering design of water fountains'
            ],
            'error_analysis': {
                'sources': ['Air resistance (neglected in theory)', 'Measurement precision', 'Digital simulation approximations'],
                'improvements': ['Conduct more trials', 'Use smaller angle increments', 'Account for air resistance effects']
            }
        },
        'instructor_comments': generate_instructor_comments(lab_data, optimal_trial),
        'grade_assessment': assess_lab_performance(lab_data),
        'generated_by': 'AI Lab Assistant - Engineer Clement Ekelemchi',
        'timestamp': datetime.now().isoformat()
    }
    
    return report

def generate_instructor_comments(lab_data, optimal_trial):
    """Generate personalized instructor comments based on experimental performance"""
    comments = []
    
    # Data quality assessment
    if len(lab_data) >= 5:
        comments.append("Excellent data collection! You conducted sufficient trials to establish a clear pattern.")
    elif len(lab_data) >= 3:
        comments.append("Good data collection. Consider conducting more trials for better statistical analysis.")
    else:
        comments.append("Limited data collected. More trials would strengthen your conclusions.")
    
    # Angle range assessment
    angles = [trial['angle'] for trial in lab_data]
    angle_range = max(angles) - min(angles)
    
    if angle_range >= 40:
        comments.append("Excellent angle coverage! You explored a wide range of launch angles.")
    elif angle_range >= 20:
        comments.append("Good angle range explored. This gives a clear picture of the angle-range relationship.")
    else:
        comments.append("Consider exploring a wider range of angles to see the complete relationship.")
    
    # Optimal angle assessment
    deviation = abs(optimal_trial['angle'] - 45)
    if deviation <= 5:
        comments.append("Outstanding! Your experimental optimal angle is very close to the theoretical prediction.")
    elif deviation <= 10:
        comments.append("Good results! Your optimal angle shows reasonable agreement with theory.")
    else:
        comments.append("Interesting deviation from theory. This could be due to experimental factors or measurement precision.")
    
    # Physics understanding
    comments.append("Your results clearly demonstrate the parabolic relationship between launch angle and range.")
    comments.append("This experiment beautifully illustrates the practical applications of trigonometry in physics.")
    
    return comments

def assess_lab_performance(lab_data):
    """Assess overall lab performance and assign grade components"""
    score_components = {}
    
    # Data collection (30 points)
    if len(lab_data) >= 5:
        score_components['data_collection'] = 30
    elif len(lab_data) >= 3:
        score_components['data_collection'] = 25
    else:
        score_components['data_collection'] = 20
    
    # Experimental design (25 points)
    angles = [trial['angle'] for trial in lab_data]
    angle_range = max(angles) - min(angles)
    
    if angle_range >= 40:
        score_components['experimental_design'] = 25
    elif angle_range >= 20:
        score_components['experimental_design'] = 20
    else:
        score_components['experimental_design'] = 15
    
    # Accuracy (25 points)
    max_range = max(trial['range'] for trial in lab_data)
    optimal_trial = next(trial for trial in lab_data if trial['range'] == max_range)
    deviation = abs(optimal_trial['angle'] - 45)
    
    if deviation <= 5:
        score_components['accuracy'] = 25
    elif deviation <= 10:
        score_components['accuracy'] = 20
    else:
        score_components['accuracy'] = 15
    
    # Analysis quality (20 points)
    score_components['analysis'] = 18  # Based on systematic approach
    
    total_score = sum(score_components.values())
    
    if total_score >= 90:
        grade = 'A'
        comment = 'Excellent work! Outstanding experimental technique and analysis.'
    elif total_score >= 80:
        grade = 'B'
        comment = 'Good work! Solid experimental approach with room for minor improvements.'
    elif total_score >= 70:
        grade = 'C'
        comment = 'Satisfactory work. Consider more systematic data collection and analysis.'
    else:
        grade = 'D'
        comment = 'Needs improvement. Focus on more comprehensive data collection and analysis.'
    
    return {
        'components': score_components,
        'total_score': total_score,
        'percentage': round((total_score / 100) * 100, 1),
        'grade': grade,
        'comment': comment
    }

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug, host='0.0.0.0', port=port)