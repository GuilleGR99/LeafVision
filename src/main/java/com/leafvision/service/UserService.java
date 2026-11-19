
package com.leafvision.service;

import com.leafvision.dao.UserDAO;
import com.leafvision.model.User;
import com.leafvision.security.PasswordUtils;

import java.sql.SQLException;
import java.util.Optional;

public class UserService {

    private final UserDAO userDAO;

    public UserService() {
        this.userDAO = new UserDAO();
    }

    // Registrar un nuevo usuario
    public boolean register(String username, String password)
            throws SQLException {

        validateCredentials(username, password);

        username = username.trim();

        if (userDAO.findByUsername(username).isPresent()) {
            return false;
        }

        String passwordHash =
                PasswordUtils.hashPassword(password);

        try {
            return userDAO.create(username, passwordHash);

        } catch (SQLException e) {

            // MySQL: nombre de usuario duplicado
            if (e.getErrorCode() == 1062) {
                return false;
            }

            throw e;
        }
    }

    // Iniciar sesion
    public Optional<User> login(String username, String password)
            throws SQLException {

        if (username == null || username.trim().isEmpty()
                || password == null || password.isEmpty()) {

            return Optional.empty();
        }

        Optional<User> result =
                userDAO.findByUsername(username.trim());

        if (!result.isPresent()) {
            return Optional.empty();
        }

        User user = result.get();

        boolean validPassword = PasswordUtils.verifyPassword(
            password,
            user.getPasswordHash()
        );

        if (!validPassword) {
            return Optional.empty();
        }

        // No devolver el hash de la contrasena a la interfaz
        return Optional.of(new User(
            user.getId(),
            user.getUsername(),
            null,
            user.getCreatedAt()
        ));
    }

    // Validar los datos del registro
    private void validateCredentials(String username,
                                     String password) {

        if (username == null || username.trim().isEmpty()) {
            throw new IllegalArgumentException(
                "El nombre de usuario es obligatorio."
            );
        }

        int usernameLength = username.trim().length();

        if (usernameLength < 3 || usernameLength > 50) {
            throw new IllegalArgumentException(
                "El usuario debe tener entre 3 y 50 caracteres."
            );
        }

        if (password == null
                || password.length() < 8
                || password.length() > 128) {

            throw new IllegalArgumentException(
                "La contrasena debe tener entre 8 y 128 caracteres."
            );
        }
    }
}
