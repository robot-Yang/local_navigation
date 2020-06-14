%  describe the feasible space of (rho, alpha, phi) by sampling points

function [Rhoo, Alphaa, Phii] = feasible_space()
    k4 = 2;
    alphaBar = 20/180*pi;

    sam_len = 20;
    Rho = linspace(0, 1.5, sam_len);
    size_Rho = size(Rho);

    Rhoo = [];
    Phii = [];
    Alphaa = [];

    for rho = Rho
        phi_max = rho^2 / k4^2;
        Phi = linspace(-phi_max, phi_max, sam_len);
        for phi = Phi
            alpha_max = (1- abs(phi) / phi_max) * alphaBar;
            Alpha = linspace(-alpha_max, alpha_max, sam_len);
            conRho = linspace(0, 0, sam_len) + rho;
            conPhi = linspace(0, 0, sam_len) + phi;
            Rhoo = [Rhoo, conRho];
            Phii = [Phii, conPhi];
            Alphaa = [Alphaa, Alpha];
            size_Rhoo = size(Rhoo);
            size_Alphaa = size(Alphaa);
            size_Phii = size(Phii);
    %         Rhoo
        end
    end
    
    p = scatter3(Rhoo, Alphaa, Phii);
    legend( p, 'Sampling point', 'Location', 'NorthEast' );
    xlabel rho(m)
    ylabel alpha
    zlabel phi
    grid on
    
%     return Rhoo, Alphaa, Phii;
end