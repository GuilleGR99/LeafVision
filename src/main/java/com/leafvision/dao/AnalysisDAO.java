
package com.leafvision.dao;

import com.leafvision.config.DatabaseConnection;
import com.leafvision.model.Analysis;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class AnalysisDAO {

    // Guardar una identificacion en la base de datos
    public boolean create(Analysis analysis) throws SQLException {

        String sql = "INSERT INTO analyses "
                   + "(user_id, class_id, common_name, scientific_name, "
                   + "confidence, reference_image) "
                   + "VALUES (?, ?, ?, ?, ?, ?)";

        try (Connection connection = DatabaseConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {

            statement.setLong(1, analysis.getUserId());
            statement.setString(2, analysis.getClassId());
            statement.setString(3, analysis.getCommonName());
            statement.setString(4, analysis.getScientificName());
            statement.setBigDecimal(5, analysis.getConfidence());
            statement.setString(6, analysis.getReferenceImage());

            return statement.executeUpdate() == 1;
        }
    }

    // Recuperar el historial de un usuario
    public List<Analysis> findByUserId(long userId)
            throws SQLException {

        String sql = "SELECT id, user_id, class_id, common_name, "
                   + "scientific_name, confidence, reference_image, "
                   + "created_at FROM analyses "
                   + "WHERE user_id = ? "
                   + "ORDER BY created_at DESC, id DESC";

        List<Analysis> analyses = new ArrayList<>();

        try (Connection connection = DatabaseConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {

            statement.setLong(1, userId);

            try (ResultSet result = statement.executeQuery()) {

                while (result.next()) {
                    analyses.add(mapAnalysis(result));
                }
            }
        }

        return analyses;
    }

    // Convertir un registro de MySQL en un objeto Analysis
    private Analysis mapAnalysis(ResultSet result)
            throws SQLException {

        return new Analysis(
            result.getLong("id"),
            result.getLong("user_id"),
            result.getString("class_id"),
            result.getString("common_name"),
            result.getString("scientific_name"),
            result.getBigDecimal("confidence"),
            result.getString("reference_image"),
            result.getTimestamp("created_at").toLocalDateTime()
        );
    }
}
