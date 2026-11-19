
package com.leafvision.dao;

import com.leafvision.config.DatabaseConnection;
import com.leafvision.model.User;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Optional;

public class UserDAO {

    // Registrar un nuevo usuario
    public boolean create(String username, String passwordHash)
            throws SQLException {

        String sql = "INSERT INTO users (username, password_hash) "
                   + "VALUES (?, ?)";

        try (Connection connection = DatabaseConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {

            statement.setString(1, username);
            statement.setString(2, passwordHash);

            return statement.executeUpdate() == 1;
        }
    }

    // Buscar un usuario por su nombre
    public Optional<User> findByUsername(String username)
            throws SQLException {

        String sql = "SELECT id, username, password_hash, created_at "
                   + "FROM users WHERE username = ?";

        try (Connection connection = DatabaseConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {

            statement.setString(1, username);

            try (ResultSet result = statement.executeQuery()) {

                if (result.next()) {
                    return Optional.of(mapUser(result));
                }
            }
        }

        return Optional.empty();
    }

    // Buscar un usuario por su identificador
    public Optional<User> findById(long id) throws SQLException {

        String sql = "SELECT id, username, password_hash, created_at "
                   + "FROM users WHERE id = ?";

        try (Connection connection = DatabaseConnection.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {

            statement.setLong(1, id);

            try (ResultSet result = statement.executeQuery()) {

                if (result.next()) {
                    return Optional.of(mapUser(result));
                }
            }
        }

        return Optional.empty();
    }

    // Convertir un registro de MySQL en un objeto User
    private User mapUser(ResultSet result) throws SQLException {

        return new User(
            result.getLong("id"),
            result.getString("username"),
            result.getString("password_hash"),
            result.getTimestamp("created_at").toLocalDateTime()
        );
    }
}
