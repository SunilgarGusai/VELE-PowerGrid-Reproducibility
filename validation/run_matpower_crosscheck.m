% Executable MATPOWER 8.1 / GNU Octave DC power-flow cross-check.
% The GitHub Actions workflow sets MATPOWER_HOME and runs this script in a
% clean Ubuntu environment. Output CSVs are written to validation/artifacts/matpower.

mp_home = getenv('MATPOWER_HOME');
if isempty(mp_home)
    error('MATPOWER_HOME environment variable is not set');
end

addpath(genpath(mp_home));

repo_root = pwd();
outdir = fullfile(repo_root, 'validation', 'artifacts', 'matpower');
if ~exist(outdir, 'dir')
    mkdir(outdir);
end

cases = {'case14', 'case30', 'case39', 'case57', 'case118', 'case300'};
mpopt = mpoption('verbose', 0, 'out.all', 0);

bus_file = fullfile(outdir, 'matpower_bus_angles.csv');
branch_file = fullfile(outdir, 'matpower_branch_flows.csv');

fb = fopen(bus_file, 'w');
if fb < 0, error('Cannot open bus output file'); end
fprintf(fb, 'case,bus_id,Va_deg_matpower\n');

fr = fopen(branch_file, 'w');
if fr < 0, fclose(fb); error('Cannot open branch output file'); end
fprintf(fr, 'case,branch_id,fbus,tbus,Pf_MW_matpower,Pt_MW_matpower\n');

for c = 1:numel(cases)
    cname = cases{c};
    results = rundcpf(cname, mpopt);
    if ~isfield(results, 'success') || results.success ~= 1
        fclose(fb); fclose(fr);
        error('MATPOWER rundcpf failed for %s', cname);
    end

    % MATPOWER bus result columns: BUS_I=1, VA=9.
    for i = 1:size(results.bus, 1)
        fprintf(fb, '%s,%d,%.15g\n', cname, round(results.bus(i,1)), results.bus(i,9));
    end

    % MATPOWER solved branch result columns: F_BUS=1, T_BUS=2, PF=14, PT=16.
    for k = 1:size(results.branch, 1)
        fprintf(fr, '%s,%d,%d,%d,%.15g,%.15g\n', cname, k, ...
            round(results.branch(k,1)), round(results.branch(k,2)), ...
            results.branch(k,14), results.branch(k,16));
    end
end

fclose(fb);
fclose(fr);

fprintf('MATPOWER/Octave DC cross-check completed for %d cases.\n', numel(cases));
