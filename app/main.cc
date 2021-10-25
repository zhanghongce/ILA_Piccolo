#include "riscvIla.hpp"
using namespace ilang;

/// the function to parse commandline arguments
VerilogVerificationTargetGenerator::vtg_config_t SetConfiguration();
VerilogVerificationTargetGenerator::vtg_config_t HandleArguments(int argc, char **argv);

void verifyNibblerInstCosa(
  Ila& model,
  const std::vector<std::string> & design_files,
  const std::string & varmap,
  const std::string & instcont
  ) {
  VerilogGeneratorBase::VlgGenConfig vlg_cfg;
  // vlg_cfg.pass_node_name = true;
  vtg_cfg.CosaAddKeep = false;

  vtg_cfg.MemAbsReadAbstraction = true;
  //vtg_cfg.target_select = vtg_cfg.INST;
  //vtg_cfg.ForceInstCheckReset = true;
  vtg_cfg.WrapperPreheader = "`define BSV_NO_INITIAL_BLOCKS 1";


  std::string RootPath = "..";
  std::string VerilogPath = RootPath + "/verilog/";
  //std::string IncludePath = VerilogPath + "include/";
  std::string RefrelPath = RootPath + "/refinement/";
  std::string OutputPath = RootPath + "/verification/";

  std::vector<std::string> path_to_design_files; // update path
  for(auto && f : design_files)
    path_to_design_files.push_back( VerilogPath + f );

  VerilogVerificationTargetGenerator vg(
      {},                             // no include
      path_to_design_files,           // designs
      "mkCPU",             // top_module_name
      RefrelPath + varmap,            // variable mapping
      RefrelPath + instcont,          // conditions of start/ready
      OutputPath,                     // output path
      model.get(),                    // model
      VerilogVerificationTargetGenerator::backend_selector::COSA, // backend: COSA
      vtg_cfg,  // target generator configuration
      vlg_cfg); // verilog generator configuration

  vg.GenerateTargets();
}




int main(int argc, char **argv) {
  // TODO

  std::vector<std::string> design_files = {
    "FIFO20.v",
    "FIFO2.v",
    "mkCPU.v",
    "mkCSR_MIE.v",
    "mkCSR_MIP.v",
    "mkCSR_RegFile.v",
    "mkGPR_RegFile.v",
    "BRAM2.v",
    "mkMMU_Cache.v",
    "mkNear_Mem.v",
    "mkSoC_Map.v",
    "RegFile.v"
  };

  // build the model
  riscvILA_user piccolo;
  piccolo.addInstructions(); // 37 base integer instructions

  verify(piccolo.model, design_files, "varmap-piccolo.json", "instcond-piccolo-multi.json");

  // riscvILA_user riscvILA(0);
  return 0;
}
