const joystick = document.getElementById('joystick');
const zone = document.getElementById('joystick-zone');

zone.addEventListener('mousedown', (event) => {
    const zoneRect = zone.getBoundingClientRect();

    const centerX = zoneRect.left + zoneRect.width / 2;
    const centerY = zoneRect.top + zoneRect.height / 2;
    const maxRadius = zoneRect.width / 2 - joystick.offsetWidth / 2;

    const handleMouseMove = (e) => {
        let x = e.clientX - centerX;
        let y = e.clientY - centerY;

        const distance = Math.sqrt(x * x + y * y);

        if (distance > maxRadius) {
            const angle = Math.atan2(y, x);
            x = Math.cos(angle) * maxRadius;
            y = Math.sin(angle) * maxRadius;
        }

        joystick.style.left = `${(zoneRect.width / 2 - joystick.offsetWidth / 2) + x}px`;
        joystick.style.top = `${(zoneRect.height / 2 - joystick.offsetHeight / 2) + y}px`;

        // Tu peux envoyer ici les valeurs normalisées :
        const normX = x / maxRadius;
        const normY = -y / maxRadius; // inversé pour avoir Y positif vers le haut
        console.log("Joystick X:", normX.toFixed(2), "Y:", normY.toFixed(2));
    };

    const handleMouseUp = () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);

        // Recentrer le joystick
        joystick.style.left = `${(zoneRect.width - joystick.offsetWidth) / 2}px`;
        joystick.style.top = `${(zoneRect.height - joystick.offsetHeight) / 2}px`;

        // Envoyer valeurs nulles
        console.log("Joystick relâché → X: 0, Y: 0");
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
});
