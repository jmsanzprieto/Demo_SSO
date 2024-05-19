<main>
    <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
        <div class="col-md-12">
            <div class="alert alert-success token">El token del usuario es <br>
                <p> <?= esc($token) ?></p>
            </div>
        </div>
    </div>
        <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
        <h2>Token Decodificado</h2>
        <?php if ($decodedToken) : ?>
            <pre><?php print_r($decodedToken); ?></pre>
        <?php else : ?>
            <p>No se pudo decodificar el token.</p>
            <?php if ($error) : ?>
                <p>Error: <?php echo $error; ?></p>
            <?php endif; ?>
        <?php endif; ?>
    </div>

    <div class="row row-cols-1 row-cols-md-3 mb-3 text-center">
        <div class="col-md-12">
            <button class="btn btn-success" onclick="conectarSoo('<?= esc($token) ?>')">Acceder a la aplicación destino</button>
        </div>
    </div>

</main>