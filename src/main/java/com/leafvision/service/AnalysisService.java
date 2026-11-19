
package com.leafvision.service;

import com.leafvision.dao.AnalysisDAO;
import com.leafvision.model.Analysis;
import com.leafvision.model.User;

import java.math.BigDecimal;
import java.sql.SQLException;
import java.util.List;

public class AnalysisService {

    private final AnalysisDAO analysisDAO;

    public AnalysisService() {
        this.analysisDAO = new AnalysisDAO();
    }

    // Guardar una identificacion exitosa
    public boolean saveAnalysis(
            User authenticatedUser,
            boolean success,
            String classId,
            String commonName,
            String scientificName,
            BigDecimal confidence,
            String referenceImage) throws SQLException {

        validateUser(authenticatedUser);

        // No almacenar identificaciones fallidas
        if (!success) {
            return false;
        }

        validateAnalysis(
            classId,
            commonName,
            scientificName,
            confidence,
            referenceImage
        );

        Analysis analysis = new Analysis(
            0,
            authenticatedUser.getId(),
            classId,
            commonName,
            scientificName,
            confidence,
            referenceImage,
            null
        );

        return analysisDAO.create(analysis);
    }

    // Recuperar el historial del usuario autenticado
    public List<Analysis> getHistory(User authenticatedUser)
            throws SQLException {

        validateUser(authenticatedUser);

        return analysisDAO.findByUserId(
            authenticatedUser.getId()
        );
    }

    // Comprobar que existe un usuario valido
    private void validateUser(User user) {

        if (user == null || user.getId() <= 0) {
            throw new IllegalArgumentException(
                "Es necesario iniciar sesion."
            );
        }
    }

    // Validar los datos de la identificacion
    private void validateAnalysis(
            String classId,
            String commonName,
            String scientificName,
            BigDecimal confidence,
            String referenceImage) {

        if (classId == null || classId.trim().isEmpty()
                || classId.length() > 100) {

            throw new IllegalArgumentException(
                "Identificador de clase no valido."
            );
        }

        if (commonName == null || commonName.trim().isEmpty()
                || commonName.length() > 150) {

            throw new IllegalArgumentException(
                "Nombre comun no valido."
            );
        }

        if (scientificName == null
                || scientificName.trim().isEmpty()
                || scientificName.length() > 200) {

            throw new IllegalArgumentException(
                "Nombre cientifico no valido."
            );
        }

        if (confidence == null
                || confidence.compareTo(BigDecimal.ZERO) < 0
                || confidence.compareTo(BigDecimal.ONE) > 0) {

            throw new IllegalArgumentException(
                "La confianza debe estar entre 0 y 1."
            );
        }

        if (referenceImage != null
                && referenceImage.length() > 500) {

            throw new IllegalArgumentException(
                "Referencia de imagen demasiado larga."
            );
        }
    }
}
