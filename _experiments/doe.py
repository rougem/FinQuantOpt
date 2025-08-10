from pathlib import Path
ROOT = Path(__file__).parent.parent

doe_twolocal_common = {
    'lp_file': f'{ROOT}/data/1/31bonds/docplex-bin-avgonly.lp',
    'num_exec': 10,
    'ansatz': 'TwoLocal',
    'theta_initial': 'piby3',
    'optimizer': 'nft',
    'device':'AerSimulator',
    'max_epoch': 4,
    'shots': 2**13,
    'theta_threshold': 0.,
    }

doe_bfcd_common = {
    'lp_file': f'{ROOT}/data/1/31bonds/docplex-bin-avgonly.lp',
    'num_exec': 10,
    'ansatz': 'bfcd',
    'theta_initial': 'piby3',
    'optimizer': 'nft',
    'device':'AerSimulator',
    'max_epoch': 4,
    'shots': 2**13,
    'theta_threshold': 0.,
    }

doe_bfcdR_common = {
    'lp_file': f'{ROOT}/data/1/31bonds/docplex-bin-avgonly.lp',
    'num_exec': 10,
    'ansatz': 'bfcdR',
    'theta_initial': 'piby3',
    'optimizer': 'nft',
    'device':'AerSimulator',
    'max_epoch': 4,
    'shots': 2**13,
    'theta_threshold': 0.,
    }

doe_109qubits_common = {
    'lp_file': f'{ROOT}/data/1/109bonds/docplex-bin-avgonly.lp',
}

doe_155qubits_common = {
    'lp_file': f'{ROOT}/data/1/155bonds/docplex-bin-avgonly.lp',
}

doe_hw_common = {
    'num_exec': 1,
    'theta_threshold': .06,
}

doe = {
    # TwoLocal full entanglement
    '1/31bonds/TwoLocal1repFull_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal1repFull_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'full'},
            'alpha': 0.1,
            },
    '1/31bonds/TwoLocal2repFull_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal2repFull_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'full'},
            'alpha': 0.1,
            },
    '1/31bonds/TwoLocal3repFull_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal3repFull_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 3, 'entanglement': 'full'},
            'alpha': 0.1,
            },
    '1/31bonds/TwoLocal3repFull_piby3_AerSimulator_0.15':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal3repFull_piby3_AerSimulator_0.15',
            'ansatz_params': {'reps': 3, 'entanglement': 'full'},
            'alpha': 0.15,
            },
    '1/31bonds/TwoLocal3repFull_piby3_AerSimulator_0.2':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal3repFull_piby3_AerSimulator_0.2',
            'ansatz_params': {'reps': 3, 'entanglement': 'full'},
            'alpha': 0.2,
            },
    # Twolocal bilinear entanglement
    '1/31bonds/TwoLocal1rep_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    '1/31bonds/TwoLocal1rep_piby3_AerSimulator_0.15':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal1rep_piby3_AerSimulator_0.15',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.15,
            },
    '1/31bonds/TwoLocal1rep_piby3_AerSimulator_0.2':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal1rep_piby3_AerSimulator_0.2',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.2,
            },
    '1/31bonds/TwoLocal2rep_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal2rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    '1/31bonds/TwoLocal2rep_piby3_AerSimulator_0.15':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal2rep_piby3_AerSimulator_0.15',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.15,
            },
    '1/31bonds/TwoLocal2rep_piby3_AerSimulator_0.2':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal2rep_piby3_AerSimulator_0.2',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.2,
            },
    '1/31bonds/TwoLocal3rep_piby3_AerSimulator_0.1':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal3rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 3, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    '1/31bonds/TwoLocal3rep_piby3_AerSimulator_0.15':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal3rep_piby3_AerSimulator_0.15',
            'ansatz_params': {'reps': 3, 'entanglement': 'bilinear'},
            'alpha': 0.15,
            },
    '1/31bonds/TwoLocal3rep_piby3_AerSimulator_0.2':
        doe_twolocal_common | {
            'experiment_id': 'TwoLocal3rep_piby3_AerSimulator_0.2',
            'ansatz_params': {'reps': 3, 'entanglement': 'bilinear'},
            'alpha': 0.2,
            },
    
    # BFCD
    '1/31bonds/bfcd1rep_piby3_AerSimulator_0.1':
        doe_bfcd_common | {
            'experiment_id': 'bfcd1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    '1/31bonds/bfcd2rep_piby3_AerSimulator_0.1':
        doe_bfcd_common | {
            'experiment_id': 'bfcd2rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    '1/31bonds/bfcd3rep_piby3_AerSimulator_0.1':
        doe_bfcd_common | {
            'experiment_id': 'bfcd3rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 3, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    '1/31bonds/bfcd1rep_piby3_AerSimulator_0.15':
        doe_bfcd_common | {
            'experiment_id': 'bfcd1rep_piby3_AerSimulator_0.15',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.15,
            },
    '1/31bonds/bfcd2rep_piby3_AerSimulator_0.15':
        doe_bfcd_common | {
            'experiment_id': 'bfcd2rep_piby3_AerSimulator_0.15',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.15,
            },
    '1/31bonds/bfcd3rep_piby3_AerSimulator_0.15':
        doe_bfcd_common | {
            'experiment_id': 'bfcd3rep_piby3_AerSimulator_0.15',
            'ansatz_params': {'reps': 3, 'entanglement': 'bilinear'},
            'alpha': 0.15,
            },
    '1/31bonds/bfcd1rep_piby3_AerSimulator_0.2':
        doe_bfcd_common | {
            'experiment_id': 'bfcd1rep_piby3_AerSimulator_0.2',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.2,
            },
    '1/31bonds/bfcd2rep_piby3_AerSimulator_0.2':
        doe_bfcd_common | {
            'experiment_id': 'bfcd2rep_piby3_AerSimulator_0.2',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.2,
            },
    '1/31bonds/bfcd3rep_piby3_AerSimulator_0.2':
        doe_bfcd_common | {
            'experiment_id': 'bfcd3rep_piby3_AerSimulator_0.2',
            'ansatz_params': {'reps': 3, 'entanglement': 'bilinear'},
            'alpha': 0.2,
            },

    # Hardware
    '1/31bonds/TwoLocal2rep_piby3_kyiv_0.15': # remark: the one that's run had no theta_threshold
        doe_twolocal_common | doe_hw_common | {
            'device':'ibm_kyiv',
            'experiment_id': 'TwoLocal2rep_piby3_kyiv_0.15',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.15,
            },
    '1/31bonds/TwoLocal2rep_piby3_kyiv_0.1':
        doe_twolocal_common | doe_hw_common | {
            'device':'ibm_kyiv',
            'experiment_id': 'TwoLocal2rep_piby3_kyiv_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },

    # 109 QUBITS
    # Twolocal bilinear entanglement
    '1/109bonds/TwoLocal1rep_piby3_AerSimulator_0.1':
        doe_twolocal_common | doe_109qubits_common | {
            'experiment_id': 'TwoLocal1rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },
    '1/109bonds/TwoLocal2rep_piby3_AerSimulator_0.1':
        doe_twolocal_common | doe_109qubits_common | {
            'experiment_id': 'TwoLocal2rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },

    # Hardware
    '1/109bonds/TwoLocal2rep_color_piby3_marrakersh_0.1':
        doe_twolocal_common | doe_109qubits_common | doe_hw_common | {
            'device':'ibm_marrakesh',
            'experiment_id': 'TwoLocal2rep_color_piby3_marrakesh_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'color'},
            'alpha': 0.1,
            'max_epoch': 1,
            },
    '1/109bonds/TwoLocal2rep_color_piby3_fez_0.1':
        doe_twolocal_common | doe_109qubits_common | doe_hw_common | {
            'device':'ibm_fez',
            'experiment_id': 'TwoLocal2rep_color_piby3_fez_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'color'},
            'alpha': 0.1,
            'max_epoch': 1,
            },
    '1/109bonds/TwoLocal2rep_bilinear_piby3_fez_0.1':
        doe_twolocal_common | doe_109qubits_common | doe_hw_common | {
            'device':'ibm_fez',
            'experiment_id': 'TwoLocal2rep_bilinear_piby3_fez_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            'max_epoch': 1,
            },
    '1/109bonds/bfcdR2rep_color_piby3_marrakesh_0.1':
        doe_bfcdR_common | doe_109qubits_common | doe_hw_common | {
            'device':'ibm_marrakesh',
            'experiment_id': 'bfcdR2rep_color_piby3_marrakesh_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'color'},
            'alpha': 0.1,
            'max_epoch': 2,
            },

    # 155 QUBITS
    # Twolocal bilinear entanglement
    '1/155bonds/TwoLocal2rep_piby3_AerSimulator_0.1':
        doe_twolocal_common | doe_155qubits_common | {
            'experiment_id': 'TwoLocal2rep_piby3_AerSimulator_0.1',
            'ansatz_params': {'reps': 2, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            },

    ############ TEST ############
    '1/31bonds/test':
        doe_twolocal_common | {
            'experiment_id': 'test',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'alpha': 0.1,
            'theta_threshold': .06,
            'num_exec': 1,
            'max_epoch': 1,
            },
        
    # Custom Portfolio Problems for Vanguard Challenge
    'custom/mean_variance_31_normal': {
            'lp_file': f'{ROOT}/vanguard_problems/mean_variance_31assets_normal_risk1.0.lp',
            'experiment_id': 'mean_variance_31_normal',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },

    'custom/esg_constrained_31': {
            'lp_file': f'{ROOT}/vanguard_problems/esg_constrained_31assets_esg7.0.lp',
            'experiment_id': 'esg_constrained_31',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },

    'custom/index_tracking_31': {
            'lp_file': f'{ROOT}/vanguard_problems/index_tracking_31assets_te0.02.lp',
            'experiment_id': 'index_tracking_31',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },
    # Converted Portfolio Problems for VQE
    'converted/esg_constrained_31assets_esg7.0': {
            'lp_file': f'{ROOT}/converted_problems/esg_constrained_31assets_esg7.0.lp',
            'experiment_id': 'converted_esg_constrained_31',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },

    'converted/portfolio_31': {
            'lp_file': f'{ROOT}/converted_problems/mean_variance_31assets_normal_risk1.0_converted.lp',
            'experiment_id': 'converted_portfolio_31',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },
    'manual/portfolio_test': {
            'lp_file': f'{ROOT}/converted_problems/manual_portfolio.lp',
            'experiment_id': 'manual_portfolio_test',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },
    # 'manual/portfolio_test': {
    #         'lp_file': f'{ROOT}/converted_problems/manual_portfolio.lp',
    #         'experiment_id': 'manual_portfolio_test',
    #         'num_exec': 1,
    #         'ansatz': 'TwoLocal',
    #         'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
    #         'theta_initial': 'piby3',
    #         'optimizer': 'nft',
    #         'device': 'AerSimulator',
    #         'max_epoch': 1,           # MINIMAL - just 1 epoch
    #         'alpha': 0.1,
    #         'shots': 512,             # VERY LOW shots  
    #         'theta_threshold': 0.06,
    #     },
    '109assets/test': {
            'lp_file': f'{ROOT}/converted_problems/mean_variance_109assets_normal_risk1.0.lp',  # BASE filename - let the code add the suffix
            'experiment_id': '109assets_normal_risk',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 200,
            'alpha': 0.1,
            'shots': 4096,
            'theta_threshold': 0.06,
        },
    '31assets/generated': {
            'lp_file': f'{ROOT}/converted_problems/index_tracking_31assets_te0.02.lp',
            'experiment_id': '31assets_generated_test',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 8192,
            'theta_threshold': 0.06,
        },
    'custom/working_portfolio': {
            'lp_file': f'{ROOT}/vanguard_problems/working_portfolio.lp',
            'experiment_id': 'custom_working_portfolio',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },
    'scale/portfolio_109': {
            'lp_file': f'{ROOT}/converted_problems/mean_variance_109assets_normal_risk1.0_converted.lp',
            'experiment_id': 'scale_109_assets',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 6,  # Increase for larger problem
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },
    'manual/working_portfolio': {
            'lp_file': f'{ROOT}/vanguard_problems/working_portfolio.lp',
            'experiment_id': 'working_portfolio_test',
            'num_exec': 1,
            'ansatz': 'TwoLocal',
            'ansatz_params': {'reps': 1, 'entanglement': 'bilinear'},
            'theta_initial': 'piby3',
            'optimizer': 'nft',
            'device': 'AerSimulator',
            'max_epoch': 4,
            'alpha': 0.1,
            'shots': 2**13,
            'theta_threshold': 0.06,
        },
    }
