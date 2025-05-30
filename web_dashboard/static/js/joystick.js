const joystick = document.getElementById('joystick');
const zone = document.getElementById('joystick-zone');

let isDragging = false;
let isRecentering = false;

zone.addEventListener('mousedown', (event) => {
    isDragging = true;
    isRecentering = false;

    const zoneRect = zone.getBoundingClientRect();
    const centerX = zoneRect.left + zoneRect.width / 2;
    const centerY = zoneRect.top + zoneRect.height / 2;
    const maxRadius = zoneRect.width / 2 - joystick.offsetWidth / 2;

    const handleMouseMove = (e) => {
        if (!isDragging || isRecentering) return;

        let x = e.clientX - centerX;
        let y = e.clientY - centerY;

        const distance = Math.sqrt(x * x + y * y);
        if (distance > maxRadius) {
            const angle = Math.atan2(y, x);
            x = Math.cos(angle) * maxRadius;
            y = Math.sin(angle) * maxRadius;
        }

        // Déplacer le joystick
        joystick.style.left = `${(zoneRect.width / 2 - joystick.offsetWidth / 2) + x}px`;
        joystick.style.top = `${(zoneRect.height / 2 - joystick.offsetHeight / 2) + y}px`;

        // Envoyer la position normalisée
        const normX = x / maxRadius;
        const normY = -y / maxRadius;

        fetch('/joystick', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ x: normX, y: normY })
        });
        console.log("Joystick X:", normX.toFixed(2), "Y:", normY.toFixed(2));
    };

    const handleMouseUp = () => {
        if (!isDragging) return;

        isDragging = false;
        isRecentering = true;

        // Supprimer les écouteurs immédiatement
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);

        // Recentrer le joystick
        joystick.style.left = `${(zoneRect.width - joystick.offsetWidth) / 2}px`;
        joystick.style.top = `${(zoneRect.height - joystick.offsetHeight) / 2}px`;

        // Envoyer les valeurs 0 une fois que le joystick est centré
        setTimeout(() => {
            isRecentering = false;

            fetch('/joystick', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ x: 0, y: 0 })
            });
            console.log("Joystick relâché → X: 0, Y: 0");
        }, 20); // petite latence pour éviter les valeurs parasites
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
});
